#ifndef PARSARIUM_NANOSVG_HARNESS_H
#define PARSARIUM_NANOSVG_HARNESS_H
#include <stdint.h>
#include <stddef.h>
struct parsarium_svg_result { int width,height,shapes,paths; };
int parsarium_parse_svg(const uint8_t *,size_t,struct parsarium_svg_result *);
#endif
