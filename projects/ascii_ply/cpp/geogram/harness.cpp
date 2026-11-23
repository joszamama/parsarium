#include "harness.h"

#include <geogram/basic/common.h>
#include <geogram/mesh/mesh.h>
#include <geogram/mesh/mesh_io.h>

#include <algorithm>
#include <cstdlib>
#include <exception>
#include <iostream>
#include <streambuf>
#include <unistd.h>

#if __has_feature(address_sanitizer)
#include <sanitizer/lsan_interface.h>
#endif

namespace {
class QuietBuffer : public std::streambuf {
    int overflow(int ch) override { return traits_type::not_eof(ch); }
};

class QuietStdout {
    QuietBuffer sink_;
    std::streambuf *saved_;
public:
    QuietStdout() : saved_(std::cout.rdbuf(&sink_)) {}
    ~QuietStdout() { std::cout.rdbuf(saved_); }
};
}

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return false;
    QuietStdout quiet;
    static const bool initialized = []() {
#if __has_feature(address_sanitizer)
        // Geogram intentionally retains its process-wide singleton at exit.
        __lsan_disable();
#endif
        GEO::initialize();
#if __has_feature(address_sanitizer)
        __lsan_enable();
#endif
        return true;
    }();
    (void)initialized;
    char path[] = "/tmp/parsarium-geogram-XXXXXX.ply";
    int fd = mkstemps(path, 4);
    if (fd < 0) return false;
    std::size_t written = 0;
    while (written < size) {
        ssize_t count = write(fd, data + written, size - written);
        if (count <= 0) {
            close(fd);
            unlink(path);
            return false;
        }
        written += static_cast<std::size_t>(count);
    }
    if (close(fd) != 0) {
        unlink(path);
        return false;
    }

    GEO::Mesh mesh;
    GEO::MeshIOFlags flags;
    flags.set_verbose(false);
    bool parsed = false;
    try {
        parsed = GEO::mesh_load(path, mesh, flags);
        if (!parsed) result->error = "GEO::mesh_load returned false";
    } catch (const std::exception &error) {
        parsed = false;
        result->error = error.what();
    } catch (...) {
        parsed = false;
        result->error = "GEO::mesh_load threw a non-standard exception";
    }
    unlink(path);
    if (!parsed) return false;
    result->vertices = mesh.vertices.nb();
    result->faces = mesh.facets.nb();
    // Geogram keeps polygonal facets: report every vertex of the first one.
    result->face.clear();
    if (mesh.facets.nb() != 0) {
        for (GEO::index_t i = 0; i < mesh.facets.nb_vertices(0); ++i)
            result->face.push_back(mesh.facets.vertex(0, i));
    }
    return true;
}
