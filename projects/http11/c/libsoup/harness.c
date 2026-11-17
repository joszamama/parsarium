#include "harness.h"

#include <libsoup/soup.h>
#include <string.h>

/* libsoup's HTTP/1 server reader (soup_message_io_data_read_headers) collects
 * lines until a "\n" or "\r\n" line that follows a LF, drops that blank line,
 * and rejects heads above 100 KiB. soup_headers_parse_request documents the
 * same contract: the buffer excludes the trailing blank line. Input without a
 * blank line is passed whole, as the reader does at end of stream. */
#define LIBSOUP_HEADER_SIZE_LIMIT ((size_t)100 * 1024)

static size_t request_head_length(const uint8_t *data, size_t size) {
    size_t start = 0;
    while (start < size) {
        const uint8_t *lf = memchr(data + start, '\n', size - start);
        if (!lf) break;
        size_t end = (size_t)(lf - data) + 1;
        size_t line = end - start;
        if (line == 1 && start >= 2 && data[start - 1] == '\n') return start;
        if (line == 2 && start >= 3 && data[start - 1] == '\n' && data[start] == '\r')
            return start;
        start = end;
    }
    return size;
}

int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result) {
    if (!result) return 0;
    memset(result, 0, sizeof(*result));
    if (!data || size == 0 || size > PARSARIUM_HTTP_MAX_INPUT) return 0;
    size_t head = request_head_length(data, size);
    if (head == 0 || head > LIBSOUP_HEADER_SIZE_LIMIT) return 0;
    SoupMessageHeaders *headers = soup_message_headers_new(SOUP_MESSAGE_HEADERS_REQUEST);
    char *method = NULL;
    char *path = NULL;
    SoupHTTPVersion version = SOUP_HTTP_1_0;
    guint status = soup_headers_parse_request((const char *)data, (int)head, headers,
                                              &method, &path, &version);
    int ok = status == SOUP_STATUS_OK && method && path;
    if (ok) {
        result->method = method;
        result->path = path;
        method = path = NULL;
        result->major = version == SOUP_HTTP_2_0 ? 2 : 1;
        result->minor = version == SOUP_HTTP_1_1 ? 1 : 0;
        result->host = g_strdup(soup_message_headers_get_one(headers, "Host"));
    }
    g_free(method);
    g_free(path);
    soup_message_headers_unref(headers);
    return ok;
}

void parsarium_http_result_clear(struct parsarium_http_result *result) {
    if (!result) return;
    g_free(result->method);
    g_free(result->path);
    g_free(result->host);
    memset(result, 0, sizeof(*result));
}
