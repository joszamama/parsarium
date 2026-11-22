#ifndef PARSARIUM_LIBIGL_PLY_HARNESS_H
#define PARSARIUM_LIBIGL_PLY_HARNESS_H

#include <cstddef>
#include <cstdint>
#include <vector>

struct ParsariumPlyResult {
    std::size_t vertices;
    std::size_t faces;
    // Vertex indices of the first face row; empty when readPLY returns no faces.
    std::vector<int> face;
};

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result);

#endif
