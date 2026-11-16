#ifndef PARSARIUM_ASSIMP_CPP_PLY_HARNESS_H
#define PARSARIUM_ASSIMP_CPP_PLY_HARNESS_H

#include <cstddef>
#include <cstdint>

struct ParsariumPlyResult {
    unsigned meshes;
    unsigned vertices;
    unsigned faces;
    unsigned face[3];
};

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result);

#endif
