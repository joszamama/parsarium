#ifndef PARSARIUM_LIBID3TAG_H
#define PARSARIUM_LIBID3TAG_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_id3_result { char title[64]; unsigned normalized_id3_major,frames; };
int parsarium_parse_id3(const uint8_t*,size_t,struct parsarium_id3_result*);
#endif
