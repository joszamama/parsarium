#ifndef PARSARIUM_TAGLIB_HARNESS_H
#define PARSARIUM_TAGLIB_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp3_result { char title[128]; char artist[128]; };
int parsarium_parse_mp3(const uint8_t *data,size_t size,struct parsarium_mp3_result *result);
#endif
