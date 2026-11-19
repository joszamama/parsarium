#ifndef PARSARIUM_MEDIAINFO_MP4_HARNESS_H
#define PARSARIUM_MEDIAINFO_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
/* Each field is MediaInfo's text value, or NULL when MediaInfo reports none
   (no title, no video or audio stream). width and height are the first video
   stream's pixel counts. */
struct parsarium_mp4_result {
    char *container, *title, *video, *audio, *width, *height;
};
int parsarium_parse_mp4(const uint8_t *, size_t, struct parsarium_mp4_result *);
void parsarium_free_mp4(struct parsarium_mp4_result *);
#endif
