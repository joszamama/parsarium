#ifndef PARSARIUM_STEREOKIT_PLY_HARNESS_H
#define PARSARIUM_STEREOKIT_PLY_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_ply_result {
    int subsets, vertices, indices;
    uint32_t face[3];
    float second_x;
    int second_present;
};
int parsarium_parse_ply(const uint8_t *data, size_t size, struct parsarium_ply_result *result);
#endif
