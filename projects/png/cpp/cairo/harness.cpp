#include "harness.h"
#include <cairo.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
int parsarium_parse_png(const uint8_t *data, size_t size, struct parsarium_png_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.png";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    cairo_surface_t *image = cairo_image_surface_create_from_png(path);
    unlink(path);
    int ok = cairo_surface_status(image) == CAIRO_STATUS_SUCCESS &&
             cairo_image_surface_get_width(image) == 2 && cairo_image_surface_get_height(image) == 1 &&
             cairo_image_surface_get_format(image) == CAIRO_FORMAT_ARGB32;
    if (ok) {
        cairo_surface_flush(image);
        const unsigned char *pixels = cairo_image_surface_get_data(image);
        uint32_t values[2]; memcpy(values, pixels, sizeof values);
        unsigned char *out[2] = {result->first, result->second};
        result->width = 2; result->height = 1;
        for (int i = 0; i < 2; i++) {
            out[i][0] = (values[i] >> 16) & 255; out[i][1] = (values[i] >> 8) & 255;
            out[i][2] = values[i] & 255; out[i][3] = values[i] >> 24;
        }
        result->has_second = 1;
    }
    cairo_surface_destroy(image);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result; (void)parsarium_parse_png(data, size, &result); return 0;
}
