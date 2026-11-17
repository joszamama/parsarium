#include "harness.h"

#include <libwebsockets.h>

#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

/* libwebsockets parses HTTP/1 only on a connection it owns. Every input is
 * handed to a no-listen server context through the catalog's documented path,
 * lws_adopt_socket_vhost_readbuf(): the bytes become the adopted connection's
 * initial read buffer and lws services them synchronously. One end of a local
 * AF_UNIX socketpair stands in for the connection; nothing is ever written to
 * it and no network socket is opened. LWS_CALLBACK_HTTP fires only after lws
 * has parsed the request line and headers, so every field below is read back
 * from the parsed header table.
 *
 * Harness caps, besides PARSARIUM_HTTP_MAX_INPUT:
 * - at most SERVICE_ROUNDS lws_service_fd() calls drain a request that did not
 *   finish inside adoption; the peer is shut down for writing first, so lws
 *   sees end of stream once its buffer is empty;
 * - fd_limit_per_thread is FD_LIMIT, so lws does not size an fd table from
 *   `ulimit -n`;
 * - one input at a time: lws contexts are single-threaded. */
#define SERVICE_ROUNDS 64
#define FD_LIMIT 16

struct exchange {
    struct lws *wsi; /* adopted connection of the current input */
    int destroyed;
    int captured;
    int failed; /* allocation failure while capturing */
    struct parsarium_http_result result;
};

static pthread_mutex_t call_mutex = PTHREAD_MUTEX_INITIALIZER;
static struct exchange *active;
static struct lws_context *context;
static struct lws_vhost *vhost;

static const struct {
    enum lws_token_indexes token;
    const char *name;
} methods[] = {
    {WSI_TOKEN_GET_URI, "GET"},
    {WSI_TOKEN_POST_URI, "POST"},
#if defined(LWS_WITH_HTTP_UNCOMMON_HEADERS)
    {WSI_TOKEN_OPTIONS_URI, "OPTIONS"},
    {WSI_TOKEN_PUT_URI, "PUT"},
    {WSI_TOKEN_PATCH_URI, "PATCH"},
    {WSI_TOKEN_DELETE_URI, "DELETE"},
#endif
    {WSI_TOKEN_CONNECT, "CONNECT"},
    {WSI_TOKEN_HEAD_URI, "HEAD"},
};

static char *copy_bytes(const char *value, size_t length) {
    char *out = malloc(length + 1);
    if (!out) return NULL;
    if (length) memcpy(out, value, length);
    out[length] = '\0';
    return out;
}

static char *header(struct lws *wsi, enum lws_token_indexes token) {
    int length = lws_hdr_total_length(wsi, token);
    if (length <= 0) return copy_bytes("", 0);
    char *out = malloc((size_t)length + 1);
    if (!out) return NULL;
    if (lws_hdr_copy(wsi, out, length + 1, token) < 0) {
        free(out);
        return NULL;
    }
    return out;
}

/* lws stores the query as one urldecoded fragment per argument; they are
 * rejoined here in parser order, after "?" when there is at least one. The
 * fragment count is bounded by lws's header table. */
static char *path_with_query(struct lws *wsi, const char *in, size_t in_length) {
    size_t total = in_length;
    int count = 0;
    for (;; count++) {
        int length = lws_hdr_fragment_length(wsi, WSI_TOKEN_HTTP_URI_ARGS, count);
        if (length <= 0) break;
        total += (size_t)length + 1; /* '?' or '&' before each argument */
    }
    char *out = malloc(total + 1);
    if (!out) return NULL;
    size_t used = 0;
    if (in_length) memcpy(out, in, in_length);
    used = in_length;
    for (int index = 0; index < count; index++) {
        int room = (int)(total - used); /* separator + fragment + NUL */
        int copied = lws_hdr_copy_fragment(wsi, out + used + 1, room,
                                           WSI_TOKEN_HTTP_URI_ARGS, index);
        if (copied < 0) {
            free(out);
            return NULL;
        }
        out[used] = index ? '&' : '?';
        used += (size_t)copied + 1;
    }
    out[used] = '\0';
    return out;
}

static void capture(struct lws *wsi, void *in, size_t length) {
    struct parsarium_http_result *result = &active->result;
    const char *method = "";
    for (size_t i = 0; i < sizeof(methods) / sizeof(methods[0]); i++) {
        if (lws_hdr_total_length(wsi, methods[i].token) > 0) {
            method = methods[i].name;
            break;
        }
    }
    result->method = copy_bytes(method, strlen(method));
    /* `in` is the request path after lws's urldecoding and path
     * normalization; no mounts are configured, so nothing is stripped. */
    result->path = path_with_query(wsi, in ? (const char *)in : "", in ? length : 0);
    result->host = header(wsi, WSI_TOKEN_HOST);
    if (!result->method || !result->path || !result->host) active->failed = 1;
    active->captured = 1;
}

static int on_event(struct lws *wsi, enum lws_callback_reasons reason, void *user,
                    void *in, size_t length) {
    (void)user;
    if (!active) return 0;
    switch (reason) {
    case LWS_CALLBACK_WSI_CREATE:
        if (!active->wsi) active->wsi = wsi;
        return 0;
    case LWS_CALLBACK_WSI_DESTROY:
        if (wsi == active->wsi) active->destroyed = 1;
        return 0;
    case LWS_CALLBACK_HTTP:
        if (wsi == active->wsi && !active->captured) capture(wsi, in, length);
        return 1; /* close: no response is needed */
    default:
        return 0;
    }
}

static const struct lws_protocols protocols[] = {
    {.name = "http", .callback = on_event},
    LWS_PROTOCOL_LIST_TERM,
};

/* Called with call_mutex held. */
static struct lws_vhost *vhost_instance(void) {
    if (vhost) return vhost;
    if (context) return NULL; /* created earlier without a usable vhost */
    lws_set_log_level(0, NULL);
    struct lws_context_creation_info info;
    memset(&info, 0, sizeof(info));
    info.port = CONTEXT_PORT_NO_LISTEN_SERVER;
    info.protocols = protocols;
    info.vhost_name = "parsarium";
    info.gid = (gid_t)-1;
    info.uid = (uid_t)-1;
    info.fd_limit_per_thread = FD_LIMIT;
    context = lws_create_context(&info);
    if (!context) return NULL;
    vhost = lws_get_vhost_by_name(context, "parsarium");
    return vhost;
}

int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result) {
    if (!result) return 0;
    memset(result, 0, sizeof(*result));
    if (!data || size == 0 || size > PARSARIUM_HTTP_MAX_INPUT) return 0;
    pthread_mutex_lock(&call_mutex);
    struct lws_vhost *host = vhost_instance();
    int sockets[2];
    if (!host || socketpair(AF_UNIX, SOCK_STREAM, 0, sockets) != 0) {
        pthread_mutex_unlock(&call_mutex);
        return 0;
    }
    struct exchange exchange;
    memset(&exchange, 0, sizeof(exchange));
    active = &exchange;
    /* lws owns sockets[0] from here on and closes it even if adoption fails. */
    struct lws *wsi = lws_adopt_socket_vhost_readbuf(host, sockets[0],
                                                     (const char *)data, size);
    if (wsi && !exchange.destroyed && !exchange.captured) {
        /* A request larger than one service chunk stays in the wsi's read
         * buffer. Ending the peer side makes lws see end of stream once the
         * buffer is drained, so the loop below finishes or closes the
         * request. */
        shutdown(sockets[1], SHUT_WR);
        for (int round = 0;
             round < SERVICE_ROUNDS && !exchange.destroyed && !exchange.captured;
             round++) {
            struct lws_pollfd pollfd;
            memset(&pollfd, 0, sizeof(pollfd));
            pollfd.fd = sockets[0];
            pollfd.events = LWS_POLLIN;
            pollfd.revents = LWS_POLLIN;
            lws_service_fd(context, &pollfd);
        }
    }
    /* Whatever happened above, the adopted connection does not outlive this
     * call: close it synchronously, which also closes sockets[0]. */
    if (exchange.wsi && !exchange.destroyed)
        lws_set_timeout(exchange.wsi, PENDING_TIMEOUT_CLOSE_SEND, LWS_TO_KILL_SYNC);
    active = NULL;
    pthread_mutex_unlock(&call_mutex);
    close(sockets[1]);
    if (!exchange.captured || exchange.failed) {
        parsarium_http_result_clear(&exchange.result);
        return 0;
    }
    *result = exchange.result;
    return 1;
}

void parsarium_http_result_clear(struct parsarium_http_result *result) {
    if (!result) return;
    free(result->method);
    free(result->path);
    free(result->host);
    memset(result, 0, sizeof(*result));
}

void parsarium_http_teardown(void) {
    pthread_mutex_lock(&call_mutex);
    if (context) lws_context_destroy(context);
    context = NULL;
    vhost = NULL;
    pthread_mutex_unlock(&call_mutex);
}
