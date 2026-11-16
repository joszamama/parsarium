#define _GNU_SOURCE
#include "harness.h"

#include <engine_c_api.h>
#include <log_c_api.h>
#include <scene_c_api.h>
#include <types_c_api.h>

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    // The native plugin is linked statically into libf3d; autoload registers
    // its readers, including PLYReader, with the reader factory.
    static int ready = 0;
    if (!ready) {
        f3d_log_set_verbose_level(F3D_LOG_QUIET, 0);
        f3d_engine_autoload_plugins();
        ready = 1;
    }
    // F3D selects the reader by file extension and then checks content.
    char directory[] = "/tmp/parsarium-f3d-XXXXXX";
    if (!mkdtemp(directory)) return 0;
    char path[sizeof(directory) + sizeof("/input.ply")];
    snprintf(path, sizeof(path), "%s/input.ply", directory);
    int fd = open(path, O_CREAT | O_EXCL | O_WRONLY, 0600);
    if (fd < 0) { rmdir(directory); return 0; }
    int written = 1;
    for (size_t offset = 0; offset < size;) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { written = 0; break; }
        offset += (size_t)count;
    }
    if (close(fd) != 0) written = 0;

    int okay = 0;
    f3d_engine_t *engine = written ? f3d_engine_create_none() : NULL;
    f3d_scene_t *scene = engine ? f3d_engine_get_scene(engine) : NULL;
    // f3d_scene_add returns 0 when scene::add raises load_failure_exception,
    // which covers unsupported content and reader failures.
    if (scene && f3d_scene_add(scene, path) == 1) {
        f3d_scene_info_t info;
        if (f3d_scene_get_scene_info(scene, &info) == 1) {
            result->files = info.number_of_files;
            result->actors = info.number_of_actors;
            result->points = (long long)info.number_of_points;
            result->cells = (long long)info.number_of_cells;
            okay = 1;
        }
    }
    f3d_engine_destroy(engine);
    unlink(path);
    rmdir(directory);
    return okay;
}
