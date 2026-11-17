#ifndef PARSARIUM_RESULT_H
#define PARSARIUM_RESULT_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_result {
    char title[256];
    unsigned video_tracks, audio_tracks, width, height, sample_rate, channels, audio_streams;
};
int parsarium_parse(const uint8_t *data, size_t size, struct parsarium_result *result);
#endif
