#include "harness.h"

#include <OpenMesh/Core/IO/MeshIO.hh>
#include <OpenMesh/Core/Mesh/TriMesh_ArrayKernelT.hh>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result) {
    if (!result || !data || size == 0 || size > (1u << 20)) return false;
    char path[] = "/tmp/parsarium-openmesh-XXXXXX.ply";
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

    OpenMesh::TriMesh_ArrayKernelT<> mesh;
    bool parsed = false;
    try {
        parsed = OpenMesh::IO::read_mesh(mesh, path);
    } catch (...) {
        parsed = false;
    }
    unlink(path);
    if (!parsed) return false;
    result->vertices = mesh.n_vertices();
    result->faces = mesh.n_faces();
    return true;
}
