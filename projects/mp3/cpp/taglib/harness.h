#ifndef PARSARIUM_TAGLIB_HARNESS_H
#define PARSARIUM_TAGLIB_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp3_result { int has_id3v2; char title[4096]; char artist[4096]; };
int parsarium_parse_mp3(const uint8_t *data,size_t size,struct parsarium_mp3_result *result);
#endif
