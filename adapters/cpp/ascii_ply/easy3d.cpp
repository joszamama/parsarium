#include <easy3d/core/surface_mesh.h>
#include <easy3d/fileio/surface_mesh_io.h>
#include <easy3d/util/logging.h>

#include <iostream>
#include <memory>
#include <vector>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    easy3d::logging::initialize(false, false, false, false, "", 0);
    std::unique_ptr<easy3d::SurfaceMesh> mesh(easy3d::SurfaceMeshIO::load(argv[1]));
    if (!mesh || mesh->n_faces() != 1) return 3;
    std::vector<int> face;
    for (auto vertex : mesh->vertices(*mesh->faces().begin())) {
        face.push_back(vertex.idx());
    }
    if (face.size() != 3) return 4;
    std::cout << "{\"vertices\":" << mesh->n_vertices()
              << ",\"faces\":" << mesh->n_faces()
              << ",\"face\":[" << face[0] << ',' << face[1] << ',' << face[2]
              << "]}\n";
}
