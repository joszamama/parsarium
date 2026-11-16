#ifndef PARSARIUM_CGAL_PLY_HARNESS_H
#define PARSARIUM_CGAL_PLY_HARNESS_H

#include <cstddef>
#include <cstdint>

struct ParsariumPlyResult {
    std::size_t vertices;
    std::size_t faces;
};

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result);

#endif
