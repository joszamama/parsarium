#ifndef PARSARIUM_BOOST_BEAST_HARNESS_H
#define PARSARIUM_BOOST_BEAST_HARNESS_H
#include <stddef.h>
#include <stdint.h>
#include <string>
struct parsarium_http_result { std::string method; std::string path; int major; int minor; std::string host; };
int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result);
#endif
