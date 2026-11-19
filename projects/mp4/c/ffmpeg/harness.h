#ifndef PARSARIUM_FFMPEG_MP4_HARNESS_H
#define PARSARIUM_FFMPEG_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
/* brand and title are NULL when the demuxer reports no such metadata entry;
   width and height come from the first video stream and are unset without one. */
struct parsarium_mp4_result {
  char *brand, *title;
  unsigned video_tracks, audio_tracks, width, height;
};
int parsarium_parse_mp4(const uint8_t *data, size_t size, struct parsarium_mp4_result *result);
void parsarium_free_mp4(struct parsarium_mp4_result *result);
#endif
