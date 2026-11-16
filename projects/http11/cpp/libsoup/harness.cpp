#include "harness.h"

#include <libsoup/soup.h>

#include <cstring>

namespace {

// libsoup's HTTP/1 server reader (soup_message_io_data_read_headers) collects
// lines until a "\n" or "\r\n" line that follows a LF, drops that blank line,
// and rejects heads above 100 KiB. Input without a blank line is passed whole,
// as the reader does at end of stream.
constexpr std::size_t header_size_limit = 100 * 1024;

std::size_t request_head_length(const std::uint8_t *data, std::size_t size) {
    std::size_t start = 0;
    while (start < size) {
        const void *lf = std::memchr(data + start, '\n', size - start);
        if (!lf) break;
        std::size_t end = static_cast<const std::uint8_t *>(lf) - data + 1;
        std::size_t line = end - start;
        if (line == 1 && start >= 2 && data[start - 1] == '\n') return start;
        if (line == 2 && start >= 3 && data[start - 1] == '\n' && data[start] == '\r')
            return start;
        start = end;
    }
    return size;
}

}  // namespace

bool parsarium_parse_http(const std::uint8_t *data, std::size_t size,
                          ParsariumHttpResult *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return false;
    std::size_t head = request_head_length(data, size);
    if (head == 0 || head > header_size_limit) return false;
    SoupMessageHeaders *headers = soup_message_headers_new(SOUP_MESSAGE_HEADERS_REQUEST);
    char *method = nullptr;
    char *path = nullptr;
    SoupHTTPVersion version = SOUP_HTTP_1_0;
    guint status = soup_headers_parse_request(reinterpret_cast<const char *>(data),
                                              static_cast<int>(head), headers,
                                              &method, &path, &version);
    bool ok = status == SOUP_STATUS_OK && method && path;
    if (ok) {
        result->method = method;
        result->path = path;
        result->minor = version == SOUP_HTTP_1_1 ? 1 : 0;
        const char *host = soup_message_headers_get_one(headers, "Host");
        result->has_host = host != nullptr;
        result->host = host ? host : "";
    }
    g_free(method);
    g_free(path);
    soup_message_headers_unref(headers);
    return ok;
}
