#ifndef PARSARIUM_MDAL_PLY_HARNESS_H
#define PARSARIUM_MDAL_PLY_HARNESS_H

#include <stddef.h>
#include <stdint.h>

struct parsarium_ply_result {
    int vertices;
    int faces;
    int indices[3];
};

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result);

#endif
