#include <pcl/io/ply_io.h>
#include <pcl/PolygonMesh.h>
#include <cstdio>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  pcl::PolygonMesh mesh;
  pcl::PLYReader reader;
  if (reader.read(argv[1], mesh) != 0 || mesh.polygons.size() != 1 ||
      mesh.polygons[0].vertices.size() != 3) return 1;
  const auto &face = mesh.polygons[0].vertices;
  std::printf("{\"vertices\":%u,\"faces\":%zu,\"face\":[%u,%u,%u]}\n",
              mesh.cloud.width * mesh.cloud.height, mesh.polygons.size(),
              face[0], face[1], face[2]);
  return 0;
}
