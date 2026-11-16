#include "harness.h"
#include <vips/vips.h>
#include <string.h>

int parsarium_parse_pnm(const uint8_t *data, size_t size, struct parsarium_pnm_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    if (VIPS_INIT("parsarium")) return 0;
    memset(result, 0, sizeof(*result));
    VipsImage *image = vips_image_new_from_buffer(data, size, "", NULL);
    if (!image) return 0;
    int width = vips_image_get_width(image), height = vips_image_get_height(image);
    int bands = vips_image_get_bands(image);
    size_t bytes = 0;
    unsigned char *pixels = vips_image_write_to_memory(image, &bytes);
    int ok = pixels && width > 0 && height > 0 && bands == 3 &&
             vips_image_get_format(image) == VIPS_FORMAT_UCHAR &&
             bytes >= (size_t)width * (size_t)height * (size_t)bands;
    if (ok) {
        result->width = (unsigned)width;
        result->height = (unsigned)height;
        memcpy(result->first, pixels, 3);
        if (width * height > 1) memcpy(result->second, pixels + 3, 3);
    }
    g_free(pixels);
    g_object_unref(image);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_pnm_result result;
    (void)parsarium_parse_pnm(data, size, &result);
    return 0;
}
