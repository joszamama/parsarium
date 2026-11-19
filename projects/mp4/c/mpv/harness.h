#ifndef PARSARIUM_MPV_MP4_HARNESS_H
#define PARSARIUM_MPV_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp4_result {
  char *container, *title, *video_codec, *audio_codec;
};
int parsarium_parse_mp4(const uint8_t *data, size_t size, struct parsarium_mp4_result *result);
void parsarium_free_mp4(struct parsarium_mp4_result *result);
#endif
