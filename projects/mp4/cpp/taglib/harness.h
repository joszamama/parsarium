#ifndef PARSARIUM_TAGLIB_MP4_HARNESS_H
#define PARSARIUM_TAGLIB_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
/* title is TagLib's title string (empty when the file has no title item) and
   NULL without a tag; has_duration is 0 when TagLib returns no audio properties. */
struct parsarium_mp4_result { char *title; int has_duration, duration_seconds; };
int parsarium_parse_mp4(const uint8_t *data,size_t size,struct parsarium_mp4_result *result);
void parsarium_free_mp4(struct parsarium_mp4_result *result);
#endif
