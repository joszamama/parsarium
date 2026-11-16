#ifndef PARSARIUM_FINWO_HTTP_HARNESS_H
#define PARSARIUM_FINWO_HTTP_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_http_result {
    char method[32], path[256], query[256], version[16], host[256];
};
int parsarium_parse_http(const uint8_t *data, size_t size,
                        struct parsarium_http_result *result);
#endif
