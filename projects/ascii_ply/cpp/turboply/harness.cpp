#include "harness.h"
#include <turboply.hpp>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <vector>
#include <unistd.h>

bool parsarium_parse_ply(const uint8_t *data, size_t size, parsarium_ply_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return false;
    *result = {};
    char path[] = "/tmp/parsarium-turboply-XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0) return false;
    size_t offset = 0;
    while (offset < size) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { close(fd); unlink(path); return false; }
        offset += static_cast<size_t>(count);
    }
    close(fd);
    bool ok = false;
    try {
        std::vector<std::array<float, 3>> vertices;
        std::vector<std::array<std::uint32_t, 3>> faces;
        turboply::PlyFileReader reader(path, false);
        reader.parseHeader();
        turboply::VertexSpec vertex_spec{vertices};
        turboply::FaceSpec face_spec{faces};
        turboply::bind_reader(reader, vertex_spec, face_spec);
        if (!vertices.empty() && !faces.empty()) {
            result->vertices = vertices.size();
            result->faces = faces.size();
            for (size_t i = 0; i < 3; ++i) result->face[i] = faces[0][i];
            ok = true;
        }
    } catch (...) { ok = false; }
    unlink(path);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parsarium_ply_result result;
    (void)parsarium_parse_ply(data, size, &result);
    return 0;
}
