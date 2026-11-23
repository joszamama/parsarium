#ifndef PARSARIUM_ASSETKIT_PLY_HARNESS_H
#define PARSARIUM_ASSETKIT_PLY_HARNESS_H

#include <stddef.h>
#include <stdint.h>

struct parsarium_ply_result {
    unsigned meshes;
    unsigned vertices;
    unsigned faces;
    /* Indices of the first triangle (face_count of them); none without faces. */
    unsigned face[3];
    unsigned face_count;
    /* Why parsing failed, when it does. */
    const char *error;
};

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result);

#endif
