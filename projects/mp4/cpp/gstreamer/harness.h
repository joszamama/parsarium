#ifndef PARSARIUM_RESULT_H
#define PARSARIUM_RESULT_H
#include <stddef.h>
#include <stdint.h>
/* title is NULL when the discoverer reports no title tag; width and height
   belong to the first video stream and are unset when there is none. */
struct parsarium_result {
    char *title;
    unsigned video_tracks, audio_tracks, width, height;
};
int parsarium_parse(const uint8_t *data, size_t size, struct parsarium_result *result);
void parsarium_free(struct parsarium_result *result);
#endif
