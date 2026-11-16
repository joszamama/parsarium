#ifndef PARSARIUM_MEDIAINFO_MP3_HARNESS_H
#define PARSARIUM_MEDIAINFO_MP3_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp3_result { char title[128], format[64]; int sample_rate; };
int parsarium_parse_mp3(const uint8_t *, size_t, struct parsarium_mp3_result *);
#endif
