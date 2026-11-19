#ifndef PARSARIUM_MONGOOSE_HARNESS_H
#define PARSARIUM_MONGOOSE_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_http_result {
    const char *method; size_t method_len;
    const char *uri; size_t uri_len;
    const char *query; size_t query_len;
    int major; int minor;
};
int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result);
#endif
