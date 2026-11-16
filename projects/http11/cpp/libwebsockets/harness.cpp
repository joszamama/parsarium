#include "harness.h"

#include <libwebsockets.h>

#include <sys/socket.h>
#include <unistd.h>

#include <mutex>
#include <vector>

namespace {

// libwebsockets parses HTTP/1 only on a connection it owns. Every input is
// handed to a no-listen server context through the catalog's documented path,
// lws_adopt_socket_vhost_readbuf(): the bytes become the adopted connection's
// initial read buffer and lws services them synchronously. One end of a local
// socketpair stands in for the connection; nothing is ever written to it.
// LWS_CALLBACK_HTTP fires only after lws has parsed the request line and
// headers, so every field below is read back from the parsed header table.
constexpr int service_rounds = 64;

struct Exchange {
    struct lws *wsi = nullptr;  // adopted connection of the current input
    bool destroyed = false;
    bool captured = false;
    ParsariumHttpResult result;
};

std::mutex call_mutex;  // lws contexts are single-threaded; one input at a time
Exchange *active = nullptr;

const struct {
    lws_token_indexes token;
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

std::string header(struct lws *wsi, lws_token_indexes token) {
    int length = lws_hdr_total_length(wsi, token);
    if (length <= 0) return "";
    std::vector<char> buffer(static_cast<std::size_t>(length) + 1);
    int copied = lws_hdr_copy(wsi, buffer.data(), length + 1, token);
    return copied < 0 ? "" : std::string(buffer.data(), static_cast<std::size_t>(copied));
}

// lws stores the query as one urldecoded fragment per argument; they are
// rejoined here in parser order.
std::string query(struct lws *wsi) {
    std::string out;
    for (int index = 0;; index++) {
        int length = lws_hdr_fragment_length(wsi, WSI_TOKEN_HTTP_URI_ARGS, index);
        if (length <= 0) break;
        std::vector<char> buffer(static_cast<std::size_t>(length) + 1);
        int copied = lws_hdr_copy_fragment(wsi, buffer.data(), length + 1,
                                           WSI_TOKEN_HTTP_URI_ARGS, index);
        if (copied < 0) break;
        if (!out.empty()) out += '&';
        out.append(buffer.data(), static_cast<std::size_t>(copied));
    }
    return out;
}

int on_event(struct lws *wsi, enum lws_callback_reasons reason, void *, void *in,
             size_t length) {
    if (!active) return 0;
    switch (reason) {
    case LWS_CALLBACK_WSI_CREATE:
        if (!active->wsi) active->wsi = wsi;
        return 0;
    case LWS_CALLBACK_WSI_DESTROY:
        if (wsi == active->wsi) active->destroyed = true;
        return 0;
    case LWS_CALLBACK_HTTP:
        if (wsi != active->wsi || active->captured) return 1;
        for (const auto &method : methods) {
            if (lws_hdr_total_length(wsi, method.token) > 0) {
                active->result.method = method.name;
                break;
            }
        }
        // `in` is the request path after lws's urldecoding and path
        // normalization; no mounts are configured, so nothing is stripped.
        active->result.path.assign(in ? static_cast<const char *>(in) : "", in ? length : 0);
        {
            std::string args = query(wsi);
            if (!args.empty()) active->result.path += "?" + args;
        }
        active->result.host = header(wsi, WSI_TOKEN_HOST);
        active->captured = true;
        return 1;  // close: no response is needed
    default:
        return 0;
    }
}

const struct lws_protocols protocols[] = {
    {"http", on_event, 0, 0, 0, nullptr, 0},
    LWS_PROTOCOL_LIST_TERM,
};

struct lws_vhost *vhost_instance() {
    static struct lws_vhost *vhost = [] {
        lws_set_log_level(0, nullptr);
        struct lws_context_creation_info info = {};
        info.port = CONTEXT_PORT_NO_LISTEN_SERVER;
        info.protocols = protocols;
        info.vhost_name = "parsarium";
        info.gid = static_cast<gid_t>(-1);
        info.uid = static_cast<uid_t>(-1);
        // Without this lws sizes an fd-indexed table from `ulimit -n`; the
        // limit switches it to a short list valid for any fd number.
        info.fd_limit_per_thread = 16;
        struct lws_context *context = lws_create_context(&info);
        if (!context) return static_cast<struct lws_vhost *>(nullptr);
        return lws_get_vhost_by_name(context, "parsarium");
    }();
    return vhost;
}

}  // namespace

bool parsarium_parse_http(const std::uint8_t *data, std::size_t size,
                          ParsariumHttpResult *result) {
    if (!result || !data || size == 0 || size > (1u << 20)) return false;
    std::lock_guard<std::mutex> call(call_mutex);
    struct lws_vhost *vhost = vhost_instance();
    if (!vhost) return false;
    int sockets[2];
    if (socketpair(AF_UNIX, SOCK_STREAM, 0, sockets) != 0) return false;
    Exchange exchange;
    active = &exchange;
    // lws owns sockets[0] from here on and closes it even if adoption fails.
    struct lws *wsi = lws_adopt_socket_vhost_readbuf(
        vhost, sockets[0], reinterpret_cast<const char *>(data), size);
    if (wsi && !exchange.destroyed && !exchange.captured) {
        // A request larger than one service chunk stays in the wsi's read
        // buffer. Ending the peer side makes lws see end of stream once the
        // buffer is drained, so the loop below finishes or closes the request.
        shutdown(sockets[1], SHUT_WR);
        struct lws_context *context = lws_get_context(wsi);
        for (int round = 0; round < service_rounds && !exchange.destroyed && !exchange.captured;
             round++) {
            struct lws_pollfd pollfd = {};
            pollfd.fd = sockets[0];
            pollfd.events = LWS_POLLIN;
            pollfd.revents = LWS_POLLIN;
            lws_service_fd(context, &pollfd);
        }
    }
    if (exchange.wsi && !exchange.destroyed)
        lws_set_timeout(exchange.wsi, PENDING_TIMEOUT_CLOSE_SEND, LWS_TO_KILL_SYNC);
    active = nullptr;
    close(sockets[1]);
    if (!exchange.captured) return false;
    *result = exchange.result;
    return true;
}
