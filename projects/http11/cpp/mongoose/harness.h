#ifndef PARSARIUM_MONGOOSE_HARNESS_H
#define PARSARIUM_MONGOOSE_HARNESS_H
#include <stddef.h>
#include <stdint.h>
#include <string>
struct parsarium_http_result { std::string method; std::string path; int major; int minor; };
int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result);
#endif
