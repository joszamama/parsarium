#define _GNU_SOURCE
#include "harness.h"
#include "mdal_c_compat.h"

#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result) {
    if (!result || !data || size == 0 || size > (1u << 20)) return 0;
    char path[] = "/tmp/parsarium-mdal-XXXXXX.ply";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t written = 0;
    while (written < size) {
        ssize_t count = write(fd, data + written, size - written);
        if (count <= 0) {
            close(fd);
            unlink(path);
            return 0;
        }
        written += (size_t)count;
    }
    if (close(fd) != 0) {
        unlink(path);
        return 0;
    }

    MDAL_MeshH mesh = MDAL_LoadMesh(path);
    unlink(path);
    if (!mesh) return 0;
    const char *driver = MDAL_M_driverName(mesh);
    int okay = driver && strcmp(driver, "PLY") == 0;
    if (okay) {
        MDAL_MeshFaceIteratorH faces = MDAL_M_faceIterator(mesh);
        if (!faces) {
            okay = 0;
        } else {
            int offsets[1] = {0};
            int indices[3] = {-1, -1, -1};
            int count = MDAL_FI_next(faces, 1, offsets, 3, indices);
            MDAL_FI_close(faces);
            if (count != 1 || offsets[0] != 3) {
                okay = 0;
            } else {
                result->vertices = MDAL_M_vertexCount(mesh);
                result->faces = MDAL_M_faceCount(mesh);
                memcpy(result->indices, indices, sizeof(indices));
            }
        }
    }
    MDAL_CloseMesh(mesh);
    return okay;
}
