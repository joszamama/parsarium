#ifndef PARSARIUM_MICRO_PLY_HARNESS_H
#define PARSARIUM_MICRO_PLY_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_ply_result {
    int32_t vertices, faces, converted;
    float second_x;
};
int parsarium_parse_ply(const uint8_t *data, size_t size,
                       struct parsarium_ply_result *result);
#endif
