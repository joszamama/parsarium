#include "harness.h"

#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/Surface_mesh/IO/PLY.h>

#include <cstdio>
#include <exception>
#include <iostream>
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
    // read_PLY writes its own reasons to std::cerr (verbose defaults to true),
    // but returns false without a message when Surface_mesh::add_face refuses a
    // face. Collect what it writes and add a line only when it wrote nothing.
    std::ostringstream messages;
    std::streambuf *original = std::cerr.rdbuf(messages.rdbuf());
    std::string failure;
    try {
        parsed = CGAL::IO::read_PLY(input, mesh, comments);
    } catch (const std::exception &error) {
        // CGAL assertion messages span several lines; keep the reason on one.
        failure = std::string("CGAL::IO::read_PLY threw: ") + error.what();
        for (char &c : failure)
            if (c == '\n') c = ' ';
    } catch (...) {
        failure = "CGAL::IO::read_PLY threw a non-standard exception";
    }
    std::cerr.rdbuf(original);
    if (parsed) std::fputs(messages.str().c_str(), stderr);
    if (!parsed) {
        std::string text = messages.str();
        if (!failure.empty()) text += failure + "\n";
        if (text.empty()) text = "CGAL::IO::read_PLY returned false\n";
        std::fputs(text.c_str(), stderr);
        return false;
    }
    result->vertices = static_cast<std::size_t>(mesh.number_of_vertices());
    result->faces = static_cast<std::size_t>(mesh.number_of_faces());
    return true;
}
