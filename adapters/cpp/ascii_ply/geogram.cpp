#include <geogram/basic/common.h>
#include <geogram/mesh/mesh.h>
#include <geogram/mesh/mesh_io.h>

#include <iostream>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    GEO::initialize();
    GEO::Mesh mesh;
    GEO::MeshIOFlags flags;
    flags.set_verbose(false);
    if (!GEO::mesh_load(argv[1], mesh, flags)) return 3;
    if (mesh.facets.nb() != 1 || mesh.facets.nb_vertices(0) != 3) return 4;
    std::cout << "{\"vertices\":" << mesh.vertices.nb()
              << ",\"faces\":" << mesh.facets.nb()
              << ",\"face\":[" << mesh.facets.vertex(0, 0) << ','
              << mesh.facets.vertex(0, 1) << ',' << mesh.facets.vertex(0, 2)
              << "]}\n";
}
