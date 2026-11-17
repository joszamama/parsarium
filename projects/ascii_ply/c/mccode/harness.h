#ifndef PARSARIUM_MCCODE_HARNESS_H
#define PARSARIUM_MCCODE_HARNESS_H
#include <stddef.h>
#include <stdint.h>

struct parsarium_ply_result {
    long vertices;
    long faces;
    double length;
    double width;
};

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result);
#endif
