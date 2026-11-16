#ifndef PARSARIUM_EASY3D_PLY_HARNESS_H
#define PARSARIUM_EASY3D_PLY_HARNESS_H

#include <cstddef>
#include <cstdint>
#include <vector>

struct ParsariumPlyResult {
    std::size_t vertices;
    std::size_t faces;
    std::vector<int> face;
};

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result);

#endif
