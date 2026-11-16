#include "harness.h"
#include <gegl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int parsarium_parse_pnm(const uint8_t *data, size_t size,
                       struct parsarium_pnm_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    *result = (struct parsarium_pnm_result){0};
    static int initialized;
    if (!initialized) {
        int argc = 1;
        char program[] = "parsarium-gegl";
        char *argv[] = {program, NULL};
        char **argvp = argv;
        gegl_init(&argc, &argvp);
        initialized = 1;
    }
    char path[] = "/tmp/parsarium-gegl-XXXXXX.ppm";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t written = 0;
    while (written < size) {
        ssize_t count = write(fd, data + written, size - written);
        if (count <= 0) { close(fd); unlink(path); return 0; }
        written += (size_t)count;
    }
    close(fd);
    GeglNode *graph = gegl_node_new();
    if (!graph) { unlink(path); return 0; }
    GeglNode *load = gegl_node_new_child(graph, "operation", "gegl:ppm-load",
                                         "path", path, NULL);
    if (!load) { g_object_unref(graph); unlink(path); return 0; }
    GeglRectangle bounds = gegl_node_get_bounding_box(load);
    int okay = 0;
    if (bounds.width >= 2 && bounds.height >= 1 &&
        bounds.width <= 4096 && bounds.height <= 4096) {
        GeglRectangle sample = {bounds.x, bounds.y, 2, 1};
        unsigned char pixels[6] = {0};
        gegl_node_blit(load, 1.0, &sample, babl_format("R'G'B' u8"), pixels,
                       GEGL_AUTO_ROWSTRIDE, GEGL_BLIT_DEFAULT);
        result->width = bounds.width;
        result->height = bounds.height;
        for (int channel = 0; channel < 3; ++channel) {
            result->first[channel] = pixels[channel];
            result->second[channel] = pixels[3 + channel];
        }
        okay = 1;
    }
    g_object_unref(graph);
    unlink(path);
    return okay;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_pnm_result result;
    (void)parsarium_parse_pnm(data, size, &result);
    return 0;
}
