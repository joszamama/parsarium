#ifndef PARSARIUM_SDL_MIXER_MP3_H
#define PARSARIUM_SDL_MIXER_MP3_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp3_result { char title[64], artist[64]; int duration_ms; };
int parsarium_parse_mp3(const uint8_t*, size_t, struct parsarium_mp3_result*);
#endif
