#ifndef PARSARIUM_MPV_MP4_HARNESS_H
#define PARSARIUM_MPV_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp4_result {
  char container[64], title[256], video_codec[32], audio_codec[32];
};
int parsarium_parse_mp4(const uint8_t *data, size_t size, struct parsarium_mp4_result *result);
#endif
