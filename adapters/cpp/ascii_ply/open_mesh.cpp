#include <OpenMesh/Core/IO/MeshIO.hh>
#include <OpenMesh/Core/Mesh/TriMesh_ArrayKernelT.hh>
#include <cstdio>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  OpenMesh::TriMesh_ArrayKernelT<> mesh;
  if (!OpenMesh::IO::read_mesh(mesh, argv[1])) return 1;
  std::printf("{\"vertices\":%zu,\"faces\":%zu}\n",
              mesh.n_vertices(), mesh.n_faces());
  return 0;
}
