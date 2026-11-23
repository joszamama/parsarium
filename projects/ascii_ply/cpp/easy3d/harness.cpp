#include "harness.h"

#include <easy3d/core/surface_mesh.h>
#include <easy3d/fileio/surface_mesh_io.h>
#include <easy3d/util/logging.h>

#include <cstdlib>
#include <exception>
#include <memory>
#include <unistd.h>

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result) {
    if (!result || !data || size == 0 || size > (1u << 20)) return false;
    static const bool logging_ready = [] {
        easy3d::logging::initialize(false, false, false, false, "", 0);
        return true;
    }();
    (void)logging_ready;
    char path[] = "/tmp/parsarium-easy3d-XXXXXX.ply";
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

    std::unique_ptr<easy3d::SurfaceMesh> mesh;
    try {
        mesh.reset(easy3d::SurfaceMeshIO::load(path));
        if (!mesh) result->error = "easy3d::SurfaceMeshIO::load returned null";
    } catch (const std::exception &error) {
        mesh.reset();
        result->error = error.what();
    } catch (...) {
        mesh.reset();
        result->error = "easy3d::SurfaceMeshIO::load threw a non-standard exception";
    }
    unlink(path);
    if (!mesh) return false;
    result->vertices = mesh->n_vertices();
    result->faces = mesh->n_faces();
    result->face.clear();
    if (result->faces != 0) {
        for (auto vertex : mesh->vertices(*mesh->faces().begin()))
            result->face.push_back(vertex.idx());
    }
    return true;
}
