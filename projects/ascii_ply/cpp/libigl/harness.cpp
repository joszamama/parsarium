#include "harness.h"

#include <igl/readPLY.h>
#include <Eigen/Core>

#include <cstdio>
#include <cstdlib>
#include <exception>
#include <unistd.h>

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         ParsariumPlyResult *result) {
    if (!result || !data || size == 0 || size > (1u << 20)) return false;
    char path[] = "/tmp/parsarium-libigl-XXXXXX.ply";
    int fd = mkstemps(path, 4);
    if (fd < 0) return false;
    std::size_t written = 0;
    while (written < size) {
        ssize_t count = write(fd, data + written, size - written);
        if (count <= 0) {
            close(fd);
            unlink(path);
            return false;
        }
        written += static_cast<std::size_t>(count);
    }
    if (close(fd) != 0) {
        unlink(path);
        return false;
    }

    Eigen::MatrixXd vertices;
    Eigen::MatrixXi faces;
    bool parsed = false;
    try {
        parsed = igl::readPLY(path, vertices, faces);
    } catch (const std::exception &error) {
        std::fprintf(stderr, "igl::readPLY threw: %s\n", error.what());
        parsed = false;
    } catch (...) {
        std::fputs("igl::readPLY threw a non-standard exception\n", stderr);
        parsed = false;
    }
    unlink(path);
    if (!parsed) return false;
    result->vertices = static_cast<std::size_t>(vertices.rows());
    result->faces = static_cast<std::size_t>(faces.rows());
    result->face.clear();
    if (faces.rows() > 0)
        for (Eigen::Index i = 0; i < faces.cols(); ++i) result->face.push_back(faces(0, i));
    return true;
}
