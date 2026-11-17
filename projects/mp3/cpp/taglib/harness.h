#ifndef PARSARIUM_TAGLIB_MP3_H
#define PARSARIUM_TAGLIB_MP3_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp3_result { unsigned version, layer, sample_rate, channels, bitrate_kbps, length_ms; };
int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result);
#endif
