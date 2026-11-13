#include "mdal_c_compat.h"

#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    MDAL_MeshH mesh = MDAL_LoadMesh(argv[1]);
    if (!mesh) return 3;
    const char *driver = MDAL_M_driverName(mesh);
    if (!driver || strcmp(driver, "PLY") != 0) {
        MDAL_CloseMesh(mesh);
        return 4;
    }
    MDAL_MeshFaceIteratorH faces = MDAL_M_faceIterator(mesh);
    if (!faces) {
        MDAL_CloseMesh(mesh);
        return 5;
    }
    int offsets[1] = {0};
    int indices[3] = {-1, -1, -1};
    int n = MDAL_FI_next(faces, 1, offsets, 3, indices);
    MDAL_FI_close(faces);
    if (n != 1 || offsets[0] != 3) {
        MDAL_CloseMesh(mesh);
        return 6;
    }
    printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[%d,%d,%d]}\n",
           MDAL_M_vertexCount(mesh), MDAL_M_faceCount(mesh),
           indices[0], indices[1], indices[2]);
    MDAL_CloseMesh(mesh);
    return 0;
}
