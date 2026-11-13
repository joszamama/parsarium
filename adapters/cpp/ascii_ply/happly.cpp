#include "happly.h"
#include <cstdio>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  try {
    happly::PLYData ply(argv[1]);
    auto vertices = ply.getVertexPositions();
    auto faces = ply.getFaceIndices<size_t>();
    if (vertices.size() != 3 || faces.size() != 1 || faces[0].size() != 3) return 1;
    std::printf("{\"vertices\":%zu,\"faces\":%zu,\"face\":[%zu,%zu,%zu]}\n",
                vertices.size(), faces.size(), faces[0][0], faces[0][1], faces[0][2]);
  } catch (...) {
    return 1;
  }
  return 0;
}
