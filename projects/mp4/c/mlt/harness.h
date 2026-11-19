#ifndef PARSARIUM_MLT_MP4_HARNESS_H
#define PARSARIUM_MLT_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp4_result {
    int streams, width, height, has_video, has_audio;
    char video_codec[64], audio_codec[64];
};
int parsarium_parse_mp4(const uint8_t *data, size_t size, struct parsarium_mp4_result *result);
#endif
