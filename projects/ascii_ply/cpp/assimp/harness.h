#ifndef PARSARIUM_ASSIMP_CPP_PLY_HARNESS_H
#define PARSARIUM_ASSIMP_CPP_PLY_HARNESS_H

#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

struct ParsariumPlyResult {
    unsigned meshes;
    unsigned vertices;
    unsigned faces;
    // All indices of the first mesh's first face; empty without a mesh or face.
    std::vector<unsigned> face;
    // Importer::GetErrorString() when the import fails.
    std::string error;
};

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result);

#endif
