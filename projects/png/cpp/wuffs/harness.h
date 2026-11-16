#ifndef PARSARIUM_WUFFS_PNG_HARNESS_H
#define PARSARIUM_WUFFS_PNG_HARNESS_H

#include <stddef.h>
#include <stdint.h>

struct parsarium_png_result { unsigned width; unsigned height; };
int parsarium_parse_png(const uint8_t *data, size_t size,
                        struct parsarium_png_result *result);

#endif
