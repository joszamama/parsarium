#ifndef PARSARIUM_MPG123_H
#define PARSARIUM_MPG123_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_mp3_result{int has_id3v2,has_title;char title[4096];unsigned id3v2_version;};
int parsarium_parse_mp3(const uint8_t*,size_t,struct parsarium_mp3_result*);
#endif
