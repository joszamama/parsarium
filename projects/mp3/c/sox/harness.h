#ifndef PARSARIUM_SOX_MP3_H
#define PARSARIUM_SOX_MP3_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp3_result{char filetype[16];unsigned sample_rate,channels,decoded_samples;};
int parsarium_parse_mp3(const uint8_t*,size_t,struct parsarium_mp3_result*);
#endif
