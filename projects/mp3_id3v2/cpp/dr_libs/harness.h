#ifndef PARSARIUM_DRMP3_HARNESS_H
#define PARSARIUM_DRMP3_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp3_result { unsigned sample_rate,channels; uint64_t decoded_frames; size_t id3v2_bytes; };
int parsarium_parse_mp3(const uint8_t *data,size_t size,struct parsarium_mp3_result *result);
#endif
