#include "harness.h"
#include <cairo.h>
#include <librsvg/rsvg.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* Rendering is bounded so a declared huge canvas cannot exhaust memory. */
#define PARSARIUM_MAX_PIXELS (4096u * 4096u)

/* Cairo ARGB32 is native-endian premultiplied; report straight RGB. */
static void copy_rgb(unsigned char output[3], const unsigned char *pixel) {
    uint32_t argb;
    memcpy(&argb, pixel, sizeof(argb));
    unsigned alpha = argb >> 24;
    for (int i = 0; i < 3; i++) {
        unsigned value = (argb >> (16 - 8 * i)) & 255;
        output[i] = alpha ? (unsigned char)((value * 255 + alpha / 2) / alpha) : 0;
    }
}

/* The documented API takes a filename, so the bytes go to a private directory.
 * librsvg only resolves relative references below the file's own directory. */
static int write_input(const uint8_t *data, size_t size, char dir[], char path[]) {
    strcpy(dir, "/tmp/parsarium-librsvg-XXXXXX");
    if (!mkdtemp(dir)) return 0;
    snprintf(path, 64, "%s/input.svg", dir);
    FILE *file = fopen(path, "wb");
    int ok = file && fwrite(data, 1, size, file) == size;
    if (file && fclose(file)) ok = 0;
    if (!ok) {
        unlink(path);
        rmdir(dir);
    }
    return ok;
}

static int render(RsvgHandle *handle, struct parsarium_svg_result *result) {
    double width = 0, height = 0;
    if (!rsvg_handle_get_intrinsic_size_in_pixels(handle, &width, &height)) return 0;
    if (!isfinite(width) || !isfinite(height) || width <= 0 || height <= 0 ||
        width > PARSARIUM_MAX_PIXELS || height > PARSARIUM_MAX_PIXELS)
        return 0;
    double surface_width = ceil(width), surface_height = ceil(height);
    if (surface_width * surface_height > PARSARIUM_MAX_PIXELS) return 0;
    int w = (int)surface_width, h = (int)surface_height;
    cairo_surface_t *surface = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, w, h);
    if (cairo_surface_status(surface) != CAIRO_STATUS_SUCCESS) {
        cairo_surface_destroy(surface);
        return 0;
    }
    cairo_t *cr = cairo_create(surface);
    RsvgRectangle viewport = {0, 0, width, height};
    GError *error = NULL;
    int ok = rsvg_handle_render_document(handle, cr, &viewport, &error) &&
             cairo_status(cr) == CAIRO_STATUS_SUCCESS;
    g_clear_error(&error);
    cairo_destroy(cr);
    if (ok) {
        cairo_surface_flush(surface);
        const unsigned char *pixels = cairo_image_surface_get_data(surface);
        int stride = cairo_image_surface_get_stride(surface);
        result->width = (unsigned)w;
        result->height = (unsigned)h;
        copy_rgb(result->first, pixels);
        result->second_present = w * h > 1;
        if (result->second_present)
            copy_rgb(result->second, w > 1 ? pixels + 4 : pixels + stride);
    }
    cairo_surface_destroy(surface);
    return ok;
}

int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char dir[64], path[64];
    if (!write_input(data, size, dir, path)) return 0;
    GError *error = NULL;
    RsvgHandle *handle = rsvg_handle_new_from_file(path, &error);
    g_clear_error(&error);
    int ok = handle && render(handle, result);
    if (handle) g_object_unref(handle);
    unlink(path);
    rmdir(dir);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_svg_result result;
    (void)parsarium_parse_svg(data, size, &result);
    return 0;
}
