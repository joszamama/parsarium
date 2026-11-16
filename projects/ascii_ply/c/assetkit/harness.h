#ifndef PARSARIUM_ASSETKIT_PLY_HARNESS_H
#define PARSARIUM_ASSETKIT_PLY_HARNESS_H

#include <stddef.h>
#include <stdint.h>

struct parsarium_ply_result {
    unsigned meshes;
    unsigned vertices;
    unsigned faces;
    unsigned face[3];
};

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result);

#endif
