#ifndef PARSARIUM_F3D_PLY_HARNESS_H
#define PARSARIUM_F3D_PLY_HARNESS_H

#include <cstddef>
#include <cstdint>

struct ParsariumPlyResult {
    long long files;
    long long actors;
    long long points;
    long long cells;
};

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result);

#endif
