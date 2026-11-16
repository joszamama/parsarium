#include "harness.h"
#define TINYPLY_IMPLEMENTATION
#include <tinyply.h>
#include <sstream>
#include <string>

bool parsarium_parse_ply(const uint8_t *data, size_t size, parsarium_ply_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return false;
    *result = {};
    try {
        std::string bytes(reinterpret_cast<const char *>(data), size);
        std::istringstream input(bytes);
        tinyply::PlyFile ply;
        if (!ply.parse_header(input) || ply.is_binary_file()) return false;
        auto vertices = ply.request_properties_from_element("vertex", {"x", "y", "z"});
        auto faces = ply.request_properties_from_element("face", {"vertex_indices"});
        ply.read(input);
        if (!vertices || !faces || vertices->count != 3 || faces->count != 1) return false;
        result->vertices = vertices->count;
        result->faces = faces->count;
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
