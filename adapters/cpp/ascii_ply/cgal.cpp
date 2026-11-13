#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/Surface_mesh/IO/PLY.h>
#include <cstdio>
#include <fstream>
#include <string>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  using Kernel = CGAL::Exact_predicates_inexact_constructions_kernel;
  CGAL::Surface_mesh<Kernel::Point_3> mesh;
  std::ifstream input(argv[1], std::ios::binary);
  std::string comments;
  if (!input || !CGAL::IO::read_PLY(input, mesh, comments)) return 1;
  std::printf("{\"vertices\":%zu,\"faces\":%zu}\n",
              static_cast<size_t>(mesh.number_of_vertices()),
              static_cast<size_t>(mesh.number_of_faces()));
  return 0;
}
