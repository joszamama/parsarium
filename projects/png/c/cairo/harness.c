#include "harness.h"
#include <cairo.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
static unsigned char cairo_float_byte(float value) {
    /* Cairo stores 16-bit PNG samples as value / 65535; report the high byte. */
    if (!(value > 0.f)) return 0;
    if (value >= 1.f) return 255;
    return (unsigned char)((unsigned)(value * 65535.f + 0.5f) >> 8);
}
static void cairo_pixel(cairo_format_t format, const unsigned char *row, int x, unsigned char out[4]) {
    if (format == CAIRO_FORMAT_RGBA128F || format == CAIRO_FORMAT_RGB96F) {
        int bands = format == CAIRO_FORMAT_RGBA128F ? 4 : 3;
        float values[4] = {0.f, 0.f, 0.f, 1.f};
        memcpy(values, row + (size_t)x * (size_t)bands * sizeof(float), (size_t)bands * sizeof(float));
        for (int i = 0; i < 4; i++) out[i] = cairo_float_byte(values[i]);
        return;
    }
    uint32_t value;
    memcpy(&value, row + (size_t)x * 4, sizeof value);
    out[0] = (value >> 16) & 255; out[1] = (value >> 8) & 255; out[2] = value & 255;
    out[3] = format == CAIRO_FORMAT_ARGB32 ? value >> 24 : 255;
}
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
    cairo_status_t status = cairo_surface_status(image);
    int ok = status == CAIRO_STATUS_SUCCESS;
    if (!ok) fprintf(stderr, "cairo: %s\n", cairo_status_to_string(status));
    if (ok) {
        cairo_surface_flush(image);
        cairo_format_t format = cairo_image_surface_get_format(image);
        int width = cairo_image_surface_get_width(image), height = cairo_image_surface_get_height(image);
        const unsigned char *pixels = cairo_image_surface_get_data(image);
        result->width = (unsigned)width; result->height = (unsigned)height;
        cairo_pixel(format, pixels, 0, result->first);
        result->has_second = width > 1;
        if (result->has_second) cairo_pixel(format, pixels, 1, result->second);
    }
    cairo_surface_destroy(image);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result; (void)parsarium_parse_png(data, size, &result); return 0;
}
