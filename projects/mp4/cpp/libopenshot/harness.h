#ifndef PARSARIUM_LIBOPENSHOT_MP4_HARNESS_H
#define PARSARIUM_LIBOPENSHOT_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp4_result {
  int video, audio, width, height;
  char video_codec[64], audio_codec[64];
};
int parsarium_parse_mp4(const uint8_t *data, size_t size, struct parsarium_mp4_result *result);
#endif
