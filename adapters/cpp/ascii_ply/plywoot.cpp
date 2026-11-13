#include <plywoot/plywoot.hpp>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <vector>

struct Vertex { double x, y, z; };
struct Triangle { std::vector<std::int32_t> indices; };

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  try {
    std::ifstream input(argv[1], std::ios::binary);
    if (!input) return 1;
    using VertexLayout = plywoot::reflect::Layout<plywoot::reflect::Pack<double, 3>>;
    using TriangleLayout = plywoot::reflect::Layout<std::vector<std::int32_t>>;
    const plywoot::IStream parser{input};
    const auto vertices = parser.readElement<Vertex, VertexLayout>();
    const auto faces = parser.readElement<Triangle, TriangleLayout>();
    if (vertices.size() != 3 || faces.size() != 1 || faces[0].indices.size() != 3)
      return 1;
    std::printf("{\"vertices\":%zu,\"faces\":%zu,\"face\":[%d,%d,%d]}\n",
                vertices.size(), faces.size(), faces[0].indices[0],
                faces[0].indices[1], faces[0].indices[2]);
  } catch (...) {
    return 1;
  }
  return 0;
}
