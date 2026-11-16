#ifndef PARSARIUM_MEDIAINFO_MP4_HARNESS_H
#define PARSARIUM_MEDIAINFO_MP4_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp4_result {
    char container[64], title[128], video[64], audio[64];
    int width, height;
};
int parsarium_parse_mp4(const uint8_t *, size_t, struct parsarium_mp4_result *);
#endif
