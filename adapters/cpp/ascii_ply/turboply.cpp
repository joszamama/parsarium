#include "turboply.hpp"
#include <array>
#include <cstdint>
#include <cstdio>
#include <vector>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  try {
    std::vector<std::array<float, 3>> vertices;
    std::vector<std::array<std::uint32_t, 3>> faces;
    turboply::PlyFileReader reader(argv[1], false);
    reader.parseHeader();
    turboply::VertexSpec vertex_spec{vertices};
    turboply::FaceSpec face_spec{faces};
    turboply::bind_reader(reader, vertex_spec, face_spec);
    if (vertices.size() != 3 || faces.size() != 1) return 1;
    std::printf("{\"vertices\":%zu,\"faces\":%zu,\"face\":[%u,%u,%u]}\n",
                vertices.size(), faces.size(), faces[0][0], faces[0][1], faces[0][2]);
  } catch (...) {
    return 1;
  }
  return 0;
}
