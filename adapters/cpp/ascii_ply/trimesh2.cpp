#include <TriMesh.h>
#include <cstdio>
#include <memory>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  std::unique_ptr<trimesh::TriMesh> mesh(trimesh::TriMesh::read(argv[1]));
  if (!mesh || mesh->faces.size() != 1 || mesh->faces[0].size() != 3) return 1;
  const auto &face = mesh->faces[0];
  std::printf("{\"vertices\":%zu,\"faces\":%zu,\"face\":[%d,%d,%d]}\n",
              mesh->vertices.size(), mesh->faces.size(), face[0], face[1], face[2]);
  return 0;
}
