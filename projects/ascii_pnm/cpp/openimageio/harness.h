#ifndef PARSARIUM_OPENIMAGEIO_PNM_H
#define PARSARIUM_OPENIMAGEIO_PNM_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_pnm_result {
    unsigned width, height, second_present;
    unsigned char first[3], second[3];
};
int parsarium_parse_pnm(const uint8_t *, size_t, struct parsarium_pnm_result *);
#endif
