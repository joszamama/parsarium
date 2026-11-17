#include "harness.h"

#include <pcl/io/ply_io.h>
#include <pcl/PolygonMesh.h>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <string>
#include <unistd.h>

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         parsarium_ply_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return false;
    char directory[] = "/tmp/parsarium-pcl-XXXXXX";
    if (!mkdtemp(directory)) return false;
    std::string path = std::string(directory) + "/input.ply";
    int fd = open(path.c_str(), O_CREAT | O_EXCL | O_WRONLY, 0600);
    if (fd < 0) { rmdir(directory); return false; }
    bool written = true;
    for (std::size_t offset = 0; offset < size;) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { written = false; break; }
        offset += static_cast<std::size_t>(count);
    }
    if (close(fd) != 0) written = false;

    bool okay = false;
    if (written) {
        pcl::PolygonMesh mesh;
        pcl::PLYReader reader;
        if (reader.read(path, mesh) == 0) {
            result->vertices = mesh.cloud.width * mesh.cloud.height;
            result->faces = mesh.polygons.size();
            result->face.clear();
            if (!mesh.polygons.empty())
                result->face.assign(mesh.polygons[0].vertices.begin(),
                                    mesh.polygons[0].vertices.end());
            okay = true;
        }
    }
    unlink(path.c_str());
    rmdir(directory);
    return okay;
}
