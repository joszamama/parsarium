#include "harness.h"
#include <happly.h>
#include <sstream>
#include <string>

bool parsarium_parse_ply(const uint8_t *data, size_t size, parsarium_ply_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return false;
    *result = {};
    try {
        std::string bytes(reinterpret_cast<const char *>(data), size);
        std::istringstream input(bytes);
        happly::PLYData ply(input);
        auto vertices = ply.getVertexPositions();
        auto faces = ply.getFaceIndices<size_t>();
        if (vertices.size() != 3 || faces.size() != 1 || faces[0].size() != 3) return false;
        result->vertices = vertices.size();
        result->faces = faces.size();
        for (size_t i = 0; i < 3; ++i) result->face[i] = faces[0][i];
        return true;
    } catch (const std::exception &) {
        return false;
    }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parsarium_ply_result result;
    (void)parsarium_parse_ply(data, size, &result);
    return 0;
}
