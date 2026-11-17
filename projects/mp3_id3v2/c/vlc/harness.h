#ifndef PARSARIUM_RESULT_H
#define PARSARIUM_RESULT_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_result {
    char title[256];
    char audio_codec[5];
    unsigned audio_tracks, mp3_tracks, rate, channels;
};
int parsarium_parse(const uint8_t *data, size_t size, struct parsarium_result *result);
#endif
