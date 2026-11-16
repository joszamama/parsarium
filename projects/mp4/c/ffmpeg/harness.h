#ifndef PARSARIUM_FFMPEG_MP4_HARNESS_H
#define PARSARIUM_FFMPEG_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp4_result {
  char brand[64], title[128];
  unsigned video_tracks, audio_tracks, width, height;
};
int parsarium_parse_mp4(const uint8_t *data, size_t size, struct parsarium_mp4_result *result);
#endif
