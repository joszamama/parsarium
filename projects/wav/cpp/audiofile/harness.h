#ifndef PARSARIUM_AUDIOFILE_HARNESS_H
#define PARSARIUM_AUDIOFILE_HARNESS_H
#include <stddef.h>
#include <stdint.h>

struct parsarium_wav_result {
    unsigned int sample_rate;
    unsigned int channels;
    unsigned long long frames;
    int16_t samples[4];
};

int parsarium_parse_wav(const uint8_t *data, size_t size,
                        struct parsarium_wav_result *result);
#endif
