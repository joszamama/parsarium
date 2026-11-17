#include "harness.h"
#include "interoff-lib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parsarium_parse_ply(const uint8_t *bytes, size_t size,
                        struct parsarium_ply_result *result) {
    if (!bytes || !result || size < 4 || size > (1u << 20) ||
        memcmp(bytes, "ply\n", 4) != 0) return 0;
    char path[] = "/tmp/parsarium-XXXXXX.ply";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, bytes + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);

    off_struct mesh;
    long faces = off_init(path, 0, 0, 0, 1, &mesh);
    unlink(path);
    if (faces <= 0 || mesh.vtxSize <= 0 || !mesh.vtxArray || !mesh.faceArray) {
        return 0;
    }
    result->vertices = mesh.vtxSize;
    result->faces = mesh.polySize;
    result->length = mesh.bbmax.x - mesh.bbmin.x;
    result->width = mesh.bbmax.y - mesh.bbmin.y;
    free(mesh.vtxArray);
    free(mesh.normalArray);
    free(mesh.DArray);
    free(mesh.faceArray);
    free(mesh.facePropArray);
    return 1;
}
