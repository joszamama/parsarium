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
        result->vertices = MDAL_M_vertexCount(mesh);
        result->faces = MDAL_M_faceCount(mesh);
        result->indices = NULL;
        result->index_count = 0;
        if (result->faces > 0) {
            /* The first face, however many vertices it has (MDAL keeps polygons). */
            int capacity = MDAL_M_faceVerticesMaximumCount(mesh);
            if (capacity < 1) capacity = 1;
            int *indices = malloc((size_t)capacity * sizeof(int));
            MDAL_MeshFaceIteratorH faces = indices ? MDAL_M_faceIterator(mesh) : NULL;
            if (!faces) {
                okay = 0;
            } else {
                int offsets[1] = {0};
                int count = MDAL_FI_next(faces, 1, offsets, capacity, indices);
                MDAL_FI_close(faces);
                if (count != 1 || offsets[0] < 0 || offsets[0] > capacity) {
                    okay = 0;
                } else {
                    result->indices = indices;
                    result->index_count = offsets[0];
                    indices = NULL;
                }
            }
            free(indices);
        }
    }
    MDAL_CloseMesh(mesh);
    return okay;
}

void parsarium_free_result(struct parsarium_ply_result *result) {
    if (!result) return;
    free(result->indices);
    result->indices = NULL;
    result->index_count = 0;
}
