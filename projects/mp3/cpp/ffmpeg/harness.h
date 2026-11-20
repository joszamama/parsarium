#ifndef PARSARIUM_FFMPEG_MP3_HARNESS_H
#define PARSARIUM_FFMPEG_MP3_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp3_result { int has_title; char title[4096]; unsigned mp3_streams; };
int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result);
#endif
