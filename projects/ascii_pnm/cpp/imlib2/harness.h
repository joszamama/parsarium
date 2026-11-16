#ifndef PARSARIUM_IMLIB2_ASCII_PNM_H
#define PARSARIUM_IMLIB2_ASCII_PNM_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_ascii_pnm_result { unsigned width, height; unsigned char first[4], second[4]; int has_second; };
int parsarium_parse_ascii_pnm(const uint8_t *data, size_t size, struct parsarium_ascii_pnm_result *result);
#endif
