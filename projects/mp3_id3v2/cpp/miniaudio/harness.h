#ifndef PARSARIUM_MINIAUDIO_MP3_HARNESS_H
#define PARSARIUM_MINIAUDIO_MP3_HARNESS_H
#include <stddef.h>
#include <stdint.h>

struct parsarium_mp3_result {
    unsigned int sample_rate;
    unsigned int channels;
    unsigned long long decoded_frames;
    unsigned long long frames;
};

int parsarium_parse_mp3(const uint8_t *data, size_t size,
                        struct parsarium_mp3_result *result);
#endif
