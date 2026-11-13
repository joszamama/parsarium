#include <engine_c_api.h>
#include <scene_c_api.h>
#include <types_c_api.h>

#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    f3d_engine_autoload_plugins();
    f3d_engine_t *engine = f3d_engine_create_none();
    if (!engine) return 3;
    f3d_scene_t *scene = f3d_engine_get_scene(engine);
    if (!scene || f3d_scene_add(scene, argv[1]) != 1) {
        f3d_engine_destroy(engine);
        return 4;
    }
    f3d_scene_info_t info;
    if (f3d_scene_get_scene_info(scene, &info) != 1) {
        f3d_engine_destroy(engine);
        return 5;
    }
    printf("{\"files\":%d,\"actors\":%d,\"points\":%lld,\"cells\":%lld}\n",
           info.number_of_files, info.number_of_actors,
           (long long)info.number_of_points, (long long)info.number_of_cells);
    f3d_engine_destroy(engine);
    return 0;
}
