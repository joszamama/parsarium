#ifndef PARSARIUM_GDK_PIXBUF_SVG_HARNESS_H
#define PARSARIUM_GDK_PIXBUF_SVG_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_svg_result {
    unsigned width, height;
    unsigned char first[4], second[4];
    int second_present;
};
int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result);
#endif
