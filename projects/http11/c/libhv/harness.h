#ifndef PARSARIUM_LIBHV_C_HARNESS_H
#define PARSARIUM_LIBHV_C_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_http_result {
    const char *method;
    size_t method_len;
    char *path;
    size_t path_len;
    int major;
    int minor;
};
int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result);
void parsarium_http_result_free(struct parsarium_http_result *result);
#endif
