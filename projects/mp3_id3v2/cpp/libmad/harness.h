#ifndef PARSARIUM_LIBMAD_MP3_H
#define PARSARIUM_LIBMAD_MP3_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp3_result { unsigned layer, sample_rate, channels, decoded_samples; unsigned long bit_rate; };
int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result);
#endif
