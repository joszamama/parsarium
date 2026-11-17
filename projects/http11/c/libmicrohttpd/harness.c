#define _GNU_SOURCE
#include "harness.h"

#include <microhttpd.h>

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <poll.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

/* libmicrohttpd parses only from a connection socket. Every input is written
 * into one end of a local socketpair whose other end is handed to a daemon
 * without a listen socket (the catalog's MHD_add_connection path). The peer
 * half-closes after the input, so MHD sees end of stream, answers or rejects
 * the request, and closes; that close is the completion signal. This is the
 * same daemon configuration as projects/http11/cpp/libmicrohttpd. */

static pthread_mutex_t call_mutex = PTHREAD_MUTEX_INITIALIZER;    /* one input at a time */
static pthread_mutex_t capture_mutex = PTHREAD_MUTEX_INITIALIZER; /* shared with MHD's thread */
static int captured;
static int current_fd = -1; /* MHD-side socket of the current input */
static struct parsarium_http_result capture;
static int request_marker;

/* Guarded by call_mutex. */
static struct MHD_Daemon *mhd;
static struct MHD_Response *empty_response;
static int hooks_registered;
/* A forked child does not inherit MHD's polling thread, so it starts its own
 * daemon. The parent's objects stay reachable here and are never touched. */
static struct MHD_Daemon *inherited_mhd;
static struct MHD_Response *inherited_response;

struct text {
    char *data;
    size_t len;
    size_t cap;
    int failed;
};

static void text_append(struct text *text, const char *bytes, size_t size) {
    if (text->failed) return;
    if (size > PARSARIUM_HTTP_MAX_CAPTURE - text->len) {
        text->failed = 1;
        return;
    }
    if (text->len + size + 1 > text->cap) {
        size_t cap = text->cap ? text->cap : 64;
        while (cap < text->len + size + 1) cap *= 2;
        if (cap > PARSARIUM_HTTP_MAX_CAPTURE + 1) cap = PARSARIUM_HTTP_MAX_CAPTURE + 1;
        char *grown = realloc(text->data, cap);
        if (!grown) {
            text->failed = 1;
            return;
        }
        text->data = grown;
        text->cap = cap;
    }
    if (size) memcpy(text->data + text->len, bytes, size);
    text->len += size;
    text->data[text->len] = '\0';
}

static void clear_capture(void) {
    free(capture.method);
    free(capture.path);
    free(capture.version);
    memset(&capture, 0, sizeof(capture));
    captured = 0;
}

static enum MHD_Result append_argument(void *cls, enum MHD_ValueKind kind,
                                       const char *key, size_t key_size,
                                       const char *value, size_t value_size) {
    (void)kind;
    struct text *query = cls;
    if (query->len) text_append(query, "&", 1);
    text_append(query, key, key_size);
    if (value) {
        text_append(query, "=", 1);
        text_append(query, value, value_size);
    }
    return query->failed ? MHD_NO : MHD_YES;
}

static enum MHD_Result on_request(void *cls, struct MHD_Connection *connection,
                                  const char *url, const char *method,
                                  const char *version, const char *upload_data,
                                  size_t *upload_data_size, void **request_closure) {
    (void)cls;
    (void)upload_data;
    if (!*request_closure) {
        *request_closure = &request_marker;
        /* MHD passes the path without its query; the query arrives as parsed
         * GET arguments, rejoined here in parser order. */
        struct text method_text = {0}, path = {0}, query = {0}, version_text = {0};
        const char *method_value = method ? method : "";
        const char *url_value = url ? url : "";
        const char *version_value = version ? version : "";
        if (strncmp(version_value, "HTTP/", 5) == 0) version_value += 5;
        text_append(&method_text, method_value, strlen(method_value));
        text_append(&path, url_value, strlen(url_value));
        text_append(&query, "", 0);
        MHD_get_connection_values_n(connection, MHD_GET_ARGUMENT_KIND, append_argument, &query);
        if (query.len) {
            text_append(&path, "?", 1);
            text_append(&path, query.data, query.len);
        }
        text_append(&version_text, version_value, strlen(version_value));
        int complete = !method_text.failed && !path.failed && !query.failed &&
                       !version_text.failed &&
                       method_text.len + path.len + version_text.len <= PARSARIUM_HTTP_MAX_CAPTURE;
        const union MHD_ConnectionInfo *info =
            MHD_get_connection_info(connection, MHD_CONNECTION_INFO_CONNECTION_FD);
        pthread_mutex_lock(&capture_mutex);
        if (complete && !captured && info && info->connect_fd == current_fd) {
            capture.method = method_text.data;
            capture.method_len = method_text.len;
            capture.path = path.data;
            capture.path_len = path.len;
            capture.version = version_text.data;
            capture.version_len = version_text.len;
            method_text.data = path.data = version_text.data = NULL;
            captured = 1;
        }
        pthread_mutex_unlock(&capture_mutex);
        free(method_text.data);
        free(path.data);
        free(query.data);
        free(version_text.data);
        return MHD_YES;
    }
    if (*upload_data_size) {
        *upload_data_size = 0;
        return MHD_YES;
    }
    return MHD_queue_response(connection, MHD_HTTP_OK, empty_response);
}

static void before_fork(void) {
    pthread_mutex_lock(&call_mutex);
    pthread_mutex_lock(&capture_mutex);
}

static void after_fork_parent(void) {
    pthread_mutex_unlock(&capture_mutex);
    pthread_mutex_unlock(&call_mutex);
}

static void after_fork_child(void) {
    if (mhd) {
        inherited_mhd = mhd;
        inherited_response = empty_response;
        mhd = NULL;
        empty_response = NULL;
    }
    current_fd = -1;
    clear_capture();
    pthread_mutex_unlock(&capture_mutex);
    pthread_mutex_unlock(&call_mutex);
}

/* Called with call_mutex held. */
static struct MHD_Daemon *daemon_instance(void) {
    if (mhd) return mhd;
    if (!hooks_registered) {
        if (pthread_atfork(before_fork, after_fork_parent, after_fork_child) != 0 ||
            atexit(parsarium_http_shutdown) != 0)
            return NULL;
        hooks_registered = 1;
    }
    empty_response = MHD_create_response_empty(MHD_RF_NONE);
    if (!empty_response) return NULL;
    mhd = MHD_start_daemon(MHD_USE_INTERNAL_POLLING_THREAD | MHD_USE_NO_LISTEN_SOCKET,
                           0, NULL, NULL, on_request, NULL,
                           MHD_OPTION_CONNECTION_TIMEOUT, (unsigned int)2,
                           MHD_OPTION_END);
    if (!mhd) {
        MHD_destroy_response(empty_response);
        empty_response = NULL;
    }
    return mhd;
}

static long remaining_ms(const struct timespec *deadline) {
    struct timespec now;
    clock_gettime(CLOCK_MONOTONIC, &now);
    return (long)(deadline->tv_sec - now.tv_sec) * 1000L +
           (deadline->tv_nsec - now.tv_nsec) / 1000000L;
}

/* Writes the input and drains replies until MHD closes its end. */
static int exchange(int peer, const uint8_t *data, size_t size) {
    int flags = fcntl(peer, F_GETFL);
    if (flags < 0 || fcntl(peer, F_SETFL, flags | O_NONBLOCK) != 0) return 0;
#ifdef SO_NOSIGPIPE
    int one = 1;
    setsockopt(peer, SOL_SOCKET, SO_NOSIGPIPE, &one, sizeof(one));
#endif
#ifdef MSG_NOSIGNAL
    const int send_flags = MSG_NOSIGNAL;
#else
    const int send_flags = 0;
#endif
    struct timespec deadline;
    clock_gettime(CLOCK_MONOTONIC, &deadline);
    deadline.tv_sec += PARSARIUM_HTTP_EXCHANGE_TIMEOUT_MS / 1000;
    deadline.tv_nsec += (long)(PARSARIUM_HTTP_EXCHANGE_TIMEOUT_MS % 1000) * 1000000L;
    if (deadline.tv_nsec >= 1000000000L) {
        deadline.tv_sec += 1;
        deadline.tv_nsec -= 1000000000L;
    }
    size_t sent = 0;
    int writing = 1;
    if (size == 0) {
        shutdown(peer, SHUT_WR);
        writing = 0;
    }
    char sink[4096];
    for (;;) {
        long left = remaining_ms(&deadline);
        if (left <= 0) return 0;
        struct pollfd fd = {peer, (short)(POLLIN | (writing ? POLLOUT : 0)), 0};
        int ready = poll(&fd, 1, (int)left);
        if (ready < 0 && errno != EINTR) return 0;
        if (ready <= 0) continue;
        if (writing && (fd.revents & (POLLOUT | POLLERR | POLLHUP))) {
            ssize_t n = send(peer, data + sent, size - sent, send_flags);
            if (n > 0) sent += (size_t)n;
            else if (n < 0 && errno != EAGAIN && errno != EWOULDBLOCK && errno != EINTR)
                writing = 0; /* MHD stopped reading (rejected or closed) */
            if (writing && sent == size) {
                shutdown(peer, SHUT_WR);
                writing = 0;
            }
        }
        if (fd.revents & (POLLIN | POLLERR | POLLHUP)) {
            ssize_t n = recv(peer, sink, sizeof(sink), 0);
            if (n == 0) return 1;
            if (n < 0 && errno != EAGAIN && errno != EWOULDBLOCK && errno != EINTR)
                return 1; /* reset by MHD: connection is gone */
        }
    }
}

/* Called with call_mutex held. */
static int parse_locked(const uint8_t *data, size_t size,
                        struct parsarium_http_result *result) {
    struct MHD_Daemon *daemon_handle = daemon_instance();
    if (!daemon_handle) return 0;
    int sockets[2];
    if (socketpair(AF_UNIX, SOCK_STREAM, 0, sockets) != 0) return 0;
    pthread_mutex_lock(&capture_mutex);
    clear_capture();
    current_fd = sockets[0];
    pthread_mutex_unlock(&capture_mutex);
    struct sockaddr_in peer_address;
    memset(&peer_address, 0, sizeof(peer_address));
    peer_address.sin_family = AF_INET;
    peer_address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    /* MHD takes ownership of sockets[0] and closes it even on failure. */
    int closed = 0;
    if (MHD_add_connection(daemon_handle, sockets[0], (const struct sockaddr *)&peer_address,
                           sizeof(peer_address)) == MHD_YES)
        closed = exchange(sockets[1], data, size);
    close(sockets[1]);
    pthread_mutex_lock(&capture_mutex);
    /* A connection that outlived the deadline keeps running inside MHD until
     * its idle timeout; resetting current_fd keeps it from being captured. */
    int ok = closed && captured;
    if (ok) {
        *result = capture;
        memset(&capture, 0, sizeof(capture));
        captured = 0;
    }
    clear_capture();
    current_fd = -1;
    pthread_mutex_unlock(&capture_mutex);
    return ok;
}

int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result) {
    if (!result) return 0;
    memset(result, 0, sizeof(*result));
    if ((!data && size) || size > PARSARIUM_HTTP_MAX_INPUT) return 0;
    pthread_mutex_lock(&call_mutex);
    int ok = parse_locked(data, size, result);
    pthread_mutex_unlock(&call_mutex);
    return ok;
}

void parsarium_http_result_clear(struct parsarium_http_result *result) {
    if (!result) return;
    free(result->method);
    free(result->path);
    free(result->version);
    memset(result, 0, sizeof(*result));
}

void parsarium_http_shutdown(void) {
    /* An exit during a parse (a sanitizer report, a fuzzer timeout) skips the
     * stop rather than wait on the input in flight. */
    if (pthread_mutex_trylock(&call_mutex) != 0) return;
    if (mhd) {
        MHD_stop_daemon(mhd);
        mhd = NULL;
    }
    if (empty_response) {
        MHD_destroy_response(empty_response);
        empty_response = NULL;
    }
    pthread_mutex_unlock(&call_mutex);
}
