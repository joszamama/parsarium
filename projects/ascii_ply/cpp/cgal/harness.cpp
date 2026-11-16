#include "harness.h"

#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/Surface_mesh/IO/PLY.h>

#include <sstream>
#include <string>

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return false;
    using Kernel = CGAL::Exact_predicates_inexact_constructions_kernel;
    CGAL::Surface_mesh<Kernel::Point_3> mesh;
    std::string bytes(reinterpret_cast<const char *>(data), size);
    std::istringstream input(bytes, std::ios::in | std::ios::binary);
    std::string comments;
    bool parsed = false;
    try {
        parsed = CGAL::IO::read_PLY(input, mesh, comments);
    } catch (...) {
        parsed = false;
    }
    if (!parsed) return false;
    result->vertices = static_cast<std::size_t>(mesh.number_of_vertices());
    result->faces = static_cast<std::size_t>(mesh.number_of_faces());
    return true;
}
