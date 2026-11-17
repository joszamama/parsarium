#ifndef PARSARIUM_JUCE_SVG_H
#define PARSARIUM_JUCE_SVG_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_svg_result { long width, height; };
int parsarium_parse_svg(const uint8_t *, size_t, struct parsarium_svg_result *);
#endif
