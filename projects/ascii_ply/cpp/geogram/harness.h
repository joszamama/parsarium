#ifndef PARSARIUM_GEOGRAM_PLY_HARNESS_H
#define PARSARIUM_GEOGRAM_PLY_HARNESS_H

#include <cstddef>
#include <cstdint>

struct ParsariumPlyResult {
    std::size_t vertices;
    std::size_t faces;
    std::size_t face_vertices;
    std::size_t face[3];
};

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result);

#endif
