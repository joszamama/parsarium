#include <geometrycentral/surface/simple_polygon_mesh.h>
#include <cstdio>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  try {
    geometrycentral::surface::SimplePolygonMesh mesh(argv[1], "ply");
    if (mesh.nVertices() != 3 || mesh.nFaces() != 1 ||
        mesh.polygons[0].size() != 3) return 1;
    std::printf("{\"vertices\":%zu,\"faces\":%zu,\"face\":[%zu,%zu,%zu]}\n",
                mesh.nVertices(), mesh.nFaces(), mesh.polygons[0][0],
                mesh.polygons[0][1], mesh.polygons[0][2]);
  } catch (...) {
    return 1;
  }
  return 0;
}
