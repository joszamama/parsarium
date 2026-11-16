#ifndef PARSARIUM_VTK_PLY_HARNESS_H
#define PARSARIUM_VTK_PLY_HARNESS_H

#include <cstddef>
#include <cstdint>
#include <vector>

struct ParsariumPlyResult {
    long long vertices;
    long long faces;
    std::vector<long long> face;
};

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result);

#endif
