#ifndef PARSARIUM_VIPS_PNM_HARNESS_H
#define PARSARIUM_VIPS_PNM_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_pnm_result {
    unsigned width, height;
    unsigned char first[3], second[3];
};
int parsarium_parse_pnm(const uint8_t *data, size_t size, struct parsarium_pnm_result *result);
#endif
