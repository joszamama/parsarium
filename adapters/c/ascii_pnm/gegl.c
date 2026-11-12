#include <gegl.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    gegl_init(&argc, &argv);
    GeglNode *graph = gegl_node_new();
    GeglNode *load = gegl_node_new_child(graph, "operation", "gegl:ppm-load",
                                         "path", argv[1], NULL);
    if (!load) return 3;
    GeglRectangle rect = gegl_node_get_bounding_box(load);
    if (rect.width != 2 || rect.height != 1) return 4;
    unsigned char pixels[6] = {0};
    gegl_node_blit(load, 1.0, &rect, babl_format("R'G'B' u8"), pixels,
                   GEGL_AUTO_ROWSTRIDE, GEGL_BLIT_DEFAULT);
    printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
           rect.width, rect.height, pixels[0], pixels[1], pixels[2],
           pixels[3], pixels[4], pixels[5]);
    g_object_unref(graph);
    gegl_exit();
    return 0;
}
