#ifndef PARSARIUM_PCL_PLY_HARNESS_H
#define PARSARIUM_PCL_PLY_HARNESS_H

#include <cstddef>
#include <cstdint>
#include <vector>

struct parsarium_ply_result {
    unsigned vertices;
    std::size_t faces;
    std::vector<unsigned> face;
};

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         parsarium_ply_result *result);

#endif
