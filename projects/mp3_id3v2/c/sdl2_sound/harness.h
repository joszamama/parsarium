#ifndef PARSARIUM_SDL2_SOUND_MP3_H
#define PARSARIUM_SDL2_SOUND_MP3_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp3_result { unsigned sample_rate, channels, decoded_bytes; int duration_ms; };
int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result);
#endif
