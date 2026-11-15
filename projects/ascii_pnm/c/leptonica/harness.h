#ifndef PARSARIUM_LEPTONICA_PNM_HARNESS_H
#define PARSARIUM_LEPTONICA_PNM_HARNESS_H

#include <stddef.h>
#include <stdint.h>

struct parsarium_pnm_result {
    int width;
    int height;
    int first_rgb[3];
    int second_rgb[3];
};

int parsarium_parse_pnm(const uint8_t *data, size_t size,
                        struct parsarium_pnm_result *result);

#endif
