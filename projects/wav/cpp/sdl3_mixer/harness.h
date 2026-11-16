#ifndef PARSARIUM_SDL3_MIXER_WAV_H
#define PARSARIUM_SDL3_MIXER_WAV_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_wav_result { unsigned sample_rate,channels; unsigned long long frames; };
int parsarium_parse_wav(const uint8_t*,size_t,struct parsarium_wav_result*);
#endif
