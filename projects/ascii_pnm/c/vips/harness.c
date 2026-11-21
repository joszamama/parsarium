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
    /* 8-bit samples for maxval up to 255, 16-bit above. The second pixel is
       the next one in raster order, if the image has one. */
    VipsBandFormat format = vips_image_get_format(image);
    size_t sample = format == VIPS_FORMAT_USHORT ? 2 : 1;
    int ok = pixels && width > 0 && height > 0 && bands == 3 &&
             (format == VIPS_FORMAT_UCHAR || format == VIPS_FORMAT_USHORT) &&
             bytes >= (size_t)width * (size_t)height * (size_t)bands * sample;
    if (ok) {
        result->width = (unsigned)width;
        result->height = (unsigned)height;
        result->has_second = (size_t)width * (size_t)height > 1;
        for (int c = 0; c < 3; ++c) {
            result->first[c] = sample == 2 ? ((const unsigned short *)pixels)[c] : pixels[c];
            if (result->has_second)
                result->second[c] = sample == 2 ? ((const unsigned short *)pixels)[3 + c] : pixels[3 + c];
        }
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
