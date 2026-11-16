#ifndef PARSARIUM_F3D_C_PLY_HARNESS_H
#define PARSARIUM_F3D_C_PLY_HARNESS_H

#include <stddef.h>
#include <stdint.h>

struct parsarium_ply_result {
    long long files;
    long long actors;
    long long points;
    long long cells;
};

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result);

#endif
