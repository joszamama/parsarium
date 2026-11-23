#ifndef PARSARIUM_GEOGRAM_PLY_HARNESS_H
#define PARSARIUM_GEOGRAM_PLY_HARNESS_H

#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

struct ParsariumPlyResult {
    std::size_t vertices;
    std::size_t faces;
    // All vertices of the first facet; empty without facets.
    std::vector<std::size_t> face;
    // Why the load failed, when it does.
    std::string error;
};

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result);

#endif
