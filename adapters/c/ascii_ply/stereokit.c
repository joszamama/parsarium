#include "stereokit_c_compat.h"
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;

    sk_settings_t settings = {0};
    settings.app_name = "Parsarium PLY control";
    settings.mode = app_mode_offscreen;
    settings.assets_folder = "";
    settings.log_filter = log_none;
    if (!sk_init(settings)) return 3;

    model_t model = model_create_file(argv[1], NULL);
    if (!model) {
        sk_shutdown();
        return 4;
    }

    int subsets = model_subset_count(model);
    mesh_t mesh = model_get_mesh(model, 0);
    if (!mesh) {
        model_release(model);
        sk_shutdown();
        return 5;
    }

    vert_t *vertices = NULL;
    vind_t *indices = NULL;
    int32_t vertex_count = 0, index_count = 0;
    mesh_get_verts(mesh, &vertices, &vertex_count, memory_reference);
    mesh_get_inds(mesh, &indices, &index_count, memory_reference);
    if (vertex_count != 3 || index_count != 3 || !vertices || !indices) {
        mesh_release(mesh);
        model_release(model);
        sk_shutdown();
        return 6;
    }

    printf("{\"subsets\":%d,\"vertices\":%d,\"indices\":%d,\"face\":[%u,%u,%u],\"second_x\":%.1f}\n",
           subsets, vertex_count, index_count, indices[0], indices[1], indices[2], vertices[1].pos.x);

    mesh_release(mesh);
    model_release(model);
    sk_shutdown();
    return 0;
}
