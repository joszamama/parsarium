#include <cairo.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    cairo_surface_t *image = cairo_image_surface_create_from_png(argv[1]);
    if (cairo_surface_status(image) != CAIRO_STATUS_SUCCESS) { cairo_surface_destroy(image); return 1; }
    int width = cairo_image_surface_get_width(image), height = cairo_image_surface_get_height(image);
    if (width != 2 || height != 1 ||
        cairo_image_surface_get_format(image) != CAIRO_FORMAT_ARGB32) {
        cairo_surface_destroy(image); return 1;
    }
    cairo_surface_flush(image);
    unsigned char *data = cairo_image_surface_get_data(image);
    uint32_t first, second;
    memcpy(&first, data, sizeof first);
    memcpy(&second, data + 4, sizeof second);
    printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           width, height, (first >> 16) & 255, (first >> 8) & 255, first & 255, first >> 24,
           (second >> 16) & 255, (second >> 8) & 255, second & 255, second >> 24);
    cairo_surface_destroy(image);
    return 0;
}
