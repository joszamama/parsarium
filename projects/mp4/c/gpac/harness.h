#ifndef PARSARIUM_GPAC_MP4_HARNESS_H
#define PARSARIUM_GPAC_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp4_result { unsigned tracks,video_tracks,audio_tracks,width,height; unsigned long long duration_ms; };
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result);
#endif
