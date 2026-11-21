#ifndef PARSARIUM_GDK_PIXBUF_PNM_H
#define PARSARIUM_GDK_PIXBUF_PNM_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_ascii_pnm_result { unsigned width, height; int has_second; unsigned char first[3], second[3]; };
int parsarium_parse_ascii_pnm(const uint8_t *data, size_t size, struct parsarium_ascii_pnm_result *result);
#endif
