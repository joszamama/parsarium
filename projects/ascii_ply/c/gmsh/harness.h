#ifndef PARSARIUM_GMSH_PLY_HARNESS_H
#define PARSARIUM_GMSH_PLY_HARNESS_H

#include <stddef.h>
#include <stdint.h>

struct parsarium_ply_result {
    size_t vertices;
    size_t triangles;
    size_t triangle_nodes;
    double x_sum;
};

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result);

#endif
