#ifndef PARSARIUM_LIBHV_HARNESS_H
#define PARSARIUM_LIBHV_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_http_result { char method[32]; char path[512]; int major; int minor; };
int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result);
#endif
