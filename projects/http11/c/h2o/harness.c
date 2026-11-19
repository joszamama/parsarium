/* H2O 2.2.6 vendors PicoHTTPParser in deps/picohttpparser; this harness calls that copy. */
#include "harness.h"
#include <picohttpparser.h>

int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    const char *method, *path;
    size_t method_len, path_len;
    struct phr_header headers[32];
    size_t header_count = sizeof(headers) / sizeof(headers[0]);
    int minor;
    /* phr_parse_request returns the length of the request head; any message
       body that follows it is not part of what PicoHTTPParser reads. */
    int consumed = phr_parse_request((const char *)data, size,
        &method, &method_len, &path, &path_len, &minor,
        headers, &header_count, 0);
    if (consumed <= 0) return 0;
    result->method = method;
    result->method_len = method_len;
    result->path = path;
    result->path_len = path_len;
    result->minor = minor;
    return 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_http_result result;
    (void)parsarium_parse_http(data, size, &result);
    return 0;
}
