#include <vcg/complex/complex.h>
#include <wrap/io_trimesh/import_ply.h>
#include <cstdio>
#include <vector>

class Vertex;
class Face;
struct Used : vcg::UsedTypes<vcg::Use<Vertex>::AsVertexType,
                             vcg::Use<Face>::AsFaceType> {};
class Vertex : public vcg::Vertex<Used, vcg::vertex::Coord3f,
                                  vcg::vertex::BitFlags> {};
class Face : public vcg::Face<Used, vcg::face::VertexRef,
                              vcg::face::BitFlags> {};
class Mesh : public vcg::tri::TriMesh<std::vector<Vertex>, std::vector<Face>> {};

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  Mesh mesh;
  if (vcg::tri::io::ImporterPLY<Mesh>::Open(mesh, argv[1]) != 0) return 1;
  if (mesh.vn != 3 || mesh.fn != 1) return 1;
  const Face &face = mesh.face[0];
  std::printf("{\"vertices\":%d,\"faces\":%d,\"face\":[%td,%td,%td]}\n",
              mesh.vn, mesh.fn, face.V(0) - &mesh.vert[0],
              face.V(1) - &mesh.vert[0], face.V(2) - &mesh.vert[0]);
  return 0;
}
