#include <cmg_c/cmg_c.h>

#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    cmg_plc *plc = NULL;
    char error[512] = {0};
    cmg_status status = cmg_read_plc(argv[1], &plc, error, sizeof error);
    if (status != CMG_OK || plc == NULL) {
        fprintf(stderr, "cmg_read_plc: %s (%d)\n", error, (int)status);
        return 1;
    }
    size_t vertices = cmg_plc_num_points(plc);
    size_t faces = cmg_plc_num_triangles(plc);
    const double *points = cmg_plc_points(plc);
    const int *triangles = cmg_plc_triangles(plc);
    if (vertices == 0 || faces == 0 || points == NULL || triangles == NULL) {
        cmg_plc_destroy(plc);
        return 1;
    }
    printf("{\"vertices\":%zu,\"faces\":%zu,\"vertex_1_x\":%.1f,\"face\":[%d,%d,%d]}\n",
           vertices, faces, points[3], triangles[0], triangles[1], triangles[2]);
    cmg_plc_destroy(plc);
    return 0;
}
