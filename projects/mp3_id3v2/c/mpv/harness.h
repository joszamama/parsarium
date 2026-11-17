#ifndef PARSARIUM_MPV_MP3_HARNESS_H
#define PARSARIUM_MPV_MP3_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp3_result {
  char title[256], codec[32];
  int64_t duration_ms;
};
int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result);
#endif
