#ifndef PARSARIUM_QTSVG_SVG_H
#define PARSARIUM_QTSVG_SVG_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_svg_result { unsigned width, height, second_present; unsigned char first[3], second[3]; };
int parsarium_parse_svg(const uint8_t *, size_t, struct parsarium_svg_result *);
#endif
