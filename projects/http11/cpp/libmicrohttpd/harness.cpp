#include "harness.h"

#include <microhttpd.h>

#include <arpa/inet.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <poll.h>
#include <sys/socket.h>
#include <unistd.h>

#include <cerrno>
#include <chrono>
#include <mutex>

namespace {

// libmicrohttpd parses only from a connection socket. Every input is written
// into one end of a local socketpair whose other end is handed to a daemon
// without a listen socket (the catalog's MHD_add_connection path). The peer
// half-closes after the input, so MHD sees end of stream, answers or rejects
// the request, and closes; that close is the completion signal.
constexpr int exchange_timeout_ms = 5000;

std::mutex call_mutex;     // one input at a time
std::mutex capture_mutex;  // shared with the MHD polling thread
bool captured = false;
int current_fd = -1;  // MHD-side socket of the current input
ParsariumHttpResult capture;
MHD_Response *empty_response = nullptr;
int request_marker;

MHD_Result append_argument(void *cls, MHD_ValueKind, const char *key, size_t key_size,
                           const char *value, size_t value_size) {
    std::string *query = static_cast<std::string *>(cls);
    if (!query->empty()) *query += '&';
    query->append(key, key_size);
    if (value) {
        *query += '=';
        query->append(value, value_size);
    }
    return MHD_YES;
}

MHD_Result on_request(void *, MHD_Connection *connection, const char *url,
                      const char *method, const char *version, const char *,
                      size_t *upload_size, void **request_closure) {
    if (!*request_closure) {
        *request_closure = &request_marker;
        // MHD passes the path without its query; the query arrives as parsed
        // GET arguments, rejoined here in parser order.
        std::string query;
        MHD_get_connection_values_n(connection, MHD_GET_ARGUMENT_KIND, append_argument, &query);
        std::string text = version ? version : "";
        if (text.compare(0, 5, "HTTP/") == 0) text.erase(0, 5);
        const MHD_ConnectionInfo *info =
            MHD_get_connection_info(connection, MHD_CONNECTION_INFO_CONNECTION_FD);
        std::lock_guard<std::mutex> lock(capture_mutex);
        if (!captured && info && info->connect_fd == current_fd) {
            captured = true;
            capture.method = method ? method : "";
            capture.path = url ? url : "";
            if (!query.empty()) capture.path += "?" + query;
            capture.version = text;
        }
        return MHD_YES;
    }
    if (*upload_size) {
        *upload_size = 0;
        return MHD_YES;
    }
    return MHD_queue_response(connection, MHD_HTTP_OK, empty_response);
}

MHD_Daemon *daemon_instance() {
    static MHD_Daemon *daemon = [] {
        empty_response = MHD_create_response_empty(MHD_RF_NONE);
        if (!empty_response) return static_cast<MHD_Daemon *>(nullptr);
        return MHD_start_daemon(MHD_USE_INTERNAL_POLLING_THREAD | MHD_USE_NO_LISTEN_SOCKET,
                                0, nullptr, nullptr, on_request, nullptr,
                                MHD_OPTION_CONNECTION_TIMEOUT, 2u, MHD_OPTION_END);
    }();
    return daemon;
}

// Writes the input and drains replies until MHD closes its end.
bool exchange(int peer, const std::uint8_t *data, std::size_t size) {
    if (fcntl(peer, F_SETFL, fcntl(peer, F_GETFL) | O_NONBLOCK) != 0) return false;
#ifdef SO_NOSIGPIPE
    int one = 1;
    setsockopt(peer, SOL_SOCKET, SO_NOSIGPIPE, &one, sizeof(one));
#endif
#ifdef MSG_NOSIGNAL
    const int send_flags = MSG_NOSIGNAL;
#else
    const int send_flags = 0;
#endif
    auto deadline = std::chrono::steady_clock::now() + std::chrono::milliseconds(exchange_timeout_ms);
    std::size_t sent = 0;
    bool writing = true;
    if (size == 0) {
        shutdown(peer, SHUT_WR);
        writing = false;
    }
    char sink[4096];
    for (;;) {
        auto left = std::chrono::duration_cast<std::chrono::milliseconds>(
            deadline - std::chrono::steady_clock::now()).count();
        if (left <= 0) return false;
        pollfd fd{peer, static_cast<short>(POLLIN | (writing ? POLLOUT : 0)), 0};
        int ready = poll(&fd, 1, static_cast<int>(left));
        if (ready < 0 && errno != EINTR) return false;
        if (ready <= 0) continue;
        if (writing && (fd.revents & (POLLOUT | POLLERR | POLLHUP))) {
            ssize_t n = send(peer, data + sent, size - sent, send_flags);
            if (n > 0) sent += static_cast<std::size_t>(n);
            else if (n < 0 && errno != EAGAIN && errno != EWOULDBLOCK && errno != EINTR)
                writing = false;  // MHD stopped reading (rejected or closed)
            if (writing && sent == size) {
                shutdown(peer, SHUT_WR);
                writing = false;
            }
        }
        if (fd.revents & (POLLIN | POLLERR | POLLHUP)) {
            ssize_t n = recv(peer, sink, sizeof(sink), 0);
            if (n == 0) return true;
            if (n < 0 && errno != EAGAIN && errno != EWOULDBLOCK && errno != EINTR)
                return true;  // reset by MHD: connection is gone
        }
    }
}

}  // namespace

bool parsarium_parse_http(const std::uint8_t *data, std::size_t size,
                          ParsariumHttpResult *result) {
    if (!result || (!data && size) || size > (1u << 20)) return false;
    std::lock_guard<std::mutex> call(call_mutex);
    MHD_Daemon *daemon = daemon_instance();
    if (!daemon) return false;
    int sockets[2];
    if (socketpair(AF_UNIX, SOCK_STREAM, 0, sockets) != 0) return false;
    {
        std::lock_guard<std::mutex> lock(capture_mutex);
        captured = false;
        capture = ParsariumHttpResult{};
        current_fd = sockets[0];
    }
    sockaddr_in peer_address{};
    peer_address.sin_family = AF_INET;
    peer_address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    // MHD takes ownership of sockets[0] and closes it even on failure.
    if (MHD_add_connection(daemon, sockets[0], reinterpret_cast<sockaddr *>(&peer_address),
                           sizeof(peer_address)) != MHD_YES) {
        close(sockets[1]);
        return false;
    }
    bool closed = exchange(sockets[1], data, size);
    close(sockets[1]);
    std::lock_guard<std::mutex> lock(capture_mutex);
    if (!closed || !captured) return false;
    *result = capture;
    return true;
}
