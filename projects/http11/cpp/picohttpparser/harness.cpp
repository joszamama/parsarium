#include "harness.h"
#include <picohttpparser.h>
#include <string.h>

int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    const char *method, *path;
    size_t method_len, path_len;
    struct phr_header headers[32];
    size_t header_count = 32;
    int minor;
    int consumed = phr_parse_request((const char *)data, size,
        &method, &method_len, &path, &path_len, &minor,
        headers, &header_count, 0);
    if (consumed != (int)size || method_len == 0 || path_len == 0 ||
        method_len >= sizeof(result->method) || path_len >= sizeof(result->path)) return 0;
    memcpy(result->method, method, method_len); result->method[method_len] = 0;
    memcpy(result->path, path, path_len); result->path[path_len] = 0;
    result->minor = minor;
    return 1;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_http_result result;
    (void)parsarium_parse_http(data, size, &result);
    return 0;
}
