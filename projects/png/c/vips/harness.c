#include "harness.h"
#include <vips/vips.h>
#include <stdio.h>
#include <string.h>

/* One 8-bit sample: 16-bit PNG samples report their high byte. */
static unsigned vips_sample(const unsigned char *pixels, VipsBandFormat format, size_t index) {
    if (format == VIPS_FORMAT_USHORT) {
        unsigned short value;
        memcpy(&value, pixels + index * sizeof value, sizeof value);
        return value >> 8;
    }
    return pixels[index];
}

/* Expand gray, gray+alpha, RGB and RGBA pixels to 8-bit RGBA. */
static void vips_pixel(const unsigned char *pixels, VipsBandFormat format, int bands, int x,
                       unsigned char out[4]) {
    size_t base = (size_t)x * (size_t)bands;
    int color = bands >= 3 ? 3 : 1;
    for (int i = 0; i < 3; i++) out[i] = (unsigned char)vips_sample(pixels, format, base + (color == 3 ? i : 0));
    out[3] = bands == 2 || bands >= 4 ? (unsigned char)vips_sample(pixels, format, base + color) : 255;
}

int parsarium_parse_png(const uint8_t *data, size_t size, struct parsarium_png_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    if (VIPS_INIT("parsarium")) return 0;
    memset(result, 0, sizeof(*result));
    VipsImage *image = vips_image_new_from_buffer(data, size, "", NULL);
    if (!image) {
        fprintf(stderr, "libvips: %s", vips_error_buffer());
        vips_error_clear();
        return 0;
    }
    int width = vips_image_get_width(image), height = vips_image_get_height(image);
    int bands = vips_image_get_bands(image);
    VipsBandFormat format = vips_image_get_format(image);
    size_t bytes = 0;
    unsigned char *pixels = vips_image_write_to_memory(image, &bytes);
    int ok = pixels != NULL;
    if (!ok) {
        fprintf(stderr, "libvips: %s", vips_error_buffer());
        vips_error_clear();
    } else if (format != VIPS_FORMAT_UCHAR && format != VIPS_FORMAT_USHORT) {
        fprintf(stderr, "harness: unexpected libvips band format %d\n", (int)format);
        ok = 0;
    }
    if (ok) {
        result->width = (unsigned)width;
        result->height = (unsigned)height;
        vips_pixel(pixels, format, bands, 0, result->first);
        result->has_second = width > 1;
        if (result->has_second) vips_pixel(pixels, format, bands, 1, result->second);
    }
    g_free(pixels);
    g_object_unref(image);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result;
    (void)parsarium_parse_png(data, size, &result);
    return 0;
}
