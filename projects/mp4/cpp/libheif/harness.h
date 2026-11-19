#ifndef PARSARIUM_LIBHEIF_MP4_HARNESS_H
#define PARSARIUM_LIBHEIF_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
/* error holds libheif's message when parsing fails. */
struct parsarium_mp4_result { unsigned sequence_tracks,video_tracks,width,height; char error[512]; };
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result);
#endif
