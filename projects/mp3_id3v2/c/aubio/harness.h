#ifndef PARSARIUM_AUBIO_MP3_HARNESS_H
#define PARSARIUM_AUBIO_MP3_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp3_result { unsigned sample_rate, channels, decoded_samples; };
int parsarium_parse_mp3(const uint8_t *, size_t, struct parsarium_mp3_result *);
#endif
