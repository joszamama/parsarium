#ifndef PARSARIUM_TAGLIB_MP4_HARNESS_H
#define PARSARIUM_TAGLIB_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp4_result { char title[128]; int duration_seconds; };
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result);
#endif
