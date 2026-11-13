#define TINYPLY_IMPLEMENTATION
#include "tinyply.h"
#include <cstdio>
#include <fstream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  try {
    std::ifstream input(argv[1], std::ios::binary);
    if (!input) return 1;
    tinyply::PlyFile ply;
    if (!ply.parse_header(input) || ply.is_binary_file()) return 1;
    auto vertices = ply.request_properties_from_element("vertex", {"x", "y", "z"});
    auto faces = ply.request_properties_from_element("face", {"vertex_indices"});
    ply.read(input);
    if (!vertices || !faces || vertices->count != 3 || faces->count != 1) return 1;
    std::printf("{\"vertices\":%zu,\"faces\":%zu}\n",
                vertices->count, faces->count);
  } catch (...) {
    return 1;
  }
  return 0;
}
