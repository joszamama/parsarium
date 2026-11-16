#ifndef PARSARIUM_GSTREAMER_PNM_HARNESS_H
#define PARSARIUM_GSTREAMER_PNM_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_pnm_result { unsigned width, height; char format[4]; unsigned char first[3], second[3]; };
int parsarium_parse_pnm(const uint8_t *, size_t, struct parsarium_pnm_result *);
#endif
