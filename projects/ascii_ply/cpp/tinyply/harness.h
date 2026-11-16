#ifndef PARSARIUM_TINYPLY_HARNESS_H
#define PARSARIUM_TINYPLY_HARNESS_H
#include <cstddef>
#include <cstdint>
struct parsarium_ply_result {
    size_t vertices;
    size_t faces;
};
bool parsarium_parse_ply(const uint8_t *data, size_t size, parsarium_ply_result *result);
#endif
