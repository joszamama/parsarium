#include "harness.h"
#include <plywoot/plywoot.hpp>
#include <cstdint>
#include <sstream>
#include <string>
#include <vector>
struct Vertex { double x, y, z; };
struct Triangle { std::vector<std::int32_t> indices; };
bool parsarium_parse_ply(const uint8_t *data, size_t size, parsarium_ply_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return false;
    *result = {};
    try {
        std::string bytes(reinterpret_cast<const char *>(data), size);
        std::istringstream input(bytes);
        using VertexLayout = plywoot::reflect::Layout<plywoot::reflect::Pack<double, 3>>;
        using TriangleLayout = plywoot::reflect::Layout<std::vector<std::int32_t>>;
        const plywoot::IStream parser{input};
        const auto vertices = parser.readElement<Vertex, VertexLayout>();
        const auto faces = parser.readElement<Triangle, TriangleLayout>();
        if (vertices.size() != 3 || faces.size() != 1 || faces[0].indices.size() != 3) return false;
        result->vertices = vertices.size();
        result->faces = faces.size();
        for (size_t i = 0; i < 3; ++i) result->face[i] = faces[0].indices[i];
        return true;
    } catch (...) { return false; }
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parsarium_ply_result result;
    (void)parsarium_parse_ply(data, size, &result);
    return 0;
}
