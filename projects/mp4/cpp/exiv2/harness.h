#ifndef PARSARIUM_EXIV2_MP4_HARNESS_H
#define PARSARIUM_EXIV2_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp4_result { char brand[64]; long width; long height; };
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result);
#endif
