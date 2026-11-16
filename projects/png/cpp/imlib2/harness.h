#ifndef PARSARIUM_IMLIB2_PNG_H
#define PARSARIUM_IMLIB2_PNG_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_png_result { unsigned width, height; unsigned char first[4], second[4]; int has_second; };
int parsarium_parse_png(const uint8_t *data, size_t size, struct parsarium_png_result *result);
#endif
