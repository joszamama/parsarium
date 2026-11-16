#include "harness.h"
#include <http-parser.h>
#include <cstdlib>
#include <cstring>

static bool copy_field(char *dest, size_t capacity, const char *source) {
    if (!source) return false;
    size_t length = std::strlen(source);
    if (length >= capacity) return false;
    std::memcpy(dest, source, length + 1);
    return true;
}

int parsarium_parse_http(const uint8_t *data, size_t size,
                        parsarium_http_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    std::memset(result, 0, sizeof(*result));
    char *bytes = static_cast<char *>(std::malloc(size + 1));
    if (!bytes) return 0;
    std::memcpy(bytes, data, size);
    bytes[size] = 0;
    struct buf input{};
    input.data = bytes; input.len = size; input.cap = size + 1;
    struct http_parser_message *request = http_parser_request_init();
    int ok = 0;
    if (request) {
        http_parser_request_data(request, &input);
        const char *host = http_parser_header_get(request, "host");
        if (request->ready &&
            copy_field(result->method, sizeof(result->method), request->method) &&
            copy_field(result->path, sizeof(result->path), request->path) &&
            copy_field(result->query, sizeof(result->query), request->query) &&
            copy_field(result->version, sizeof(result->version), request->version) &&
            copy_field(result->host, sizeof(result->host), host)) ok = 1;
        http_parser_message_free(request);
    }
    std::free(bytes);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parsarium_http_result result;
    (void)parsarium_parse_http(data, size, &result);
    return 0;
}
