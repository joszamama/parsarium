#ifndef PARSARIUM_LIBIMAGO_HARNESS_H
#define PARSARIUM_LIBIMAGO_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_pnm_result { int width, height; unsigned first[4], second[4]; };
int parsarium_parse_pnm(const uint8_t *data, size_t size, struct parsarium_pnm_result *result);
#endif
