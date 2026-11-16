#ifndef PARSARIUM_LIBPARSEHTTP_HARNESS_H
#define PARSARIUM_LIBPARSEHTTP_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_http_result {char method[16],path[256],query[128],version[16],host[128];};
int parsarium_parse_http(const uint8_t *,size_t,struct parsarium_http_result *);
#endif
