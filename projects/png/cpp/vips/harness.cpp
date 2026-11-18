#include "harness.h"
#include <vips/vips8>
#include <cstdio>
#include <cstring>

/* One 8-bit sample: 16-bit PNG samples report their high byte. */
static unsigned vips_sample(const unsigned char *pixels, VipsBandFormat format, size_t index) {
    if (format == VIPS_FORMAT_USHORT) {
        unsigned short value;
        std::memcpy(&value, pixels + index * sizeof value, sizeof value);
        return value >> 8;
    }
    return pixels[index];
}

/* Expand gray, gray+alpha, RGB and RGBA pixels to 8-bit RGBA. */
static void vips_pixel(const unsigned char *pixels, VipsBandFormat format, int bands, int x,
                       unsigned char out[4]) {
    size_t base = static_cast<size_t>(x) * static_cast<size_t>(bands);
    int color = bands >= 3 ? 3 : 1;
    for (int i = 0; i < 3; i++)
        out[i] = static_cast<unsigned char>(vips_sample(pixels, format, base + (color == 3 ? i : 0)));
    out[3] = bands == 2 || bands >= 4
        ? static_cast<unsigned char>(vips_sample(pixels, format, base + color)) : 255;
}

int parsarium_parse_png(const uint8_t *data, size_t size, struct parsarium_png_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    if (VIPS_INIT("parsarium")) return 0;
    std::memset(result, 0, sizeof(*result));
    try {
        vips::VImage image = vips::VImage::new_from_buffer(data, size, "");
        int width = image.width(), height = image.height(), bands = image.bands();
        VipsBandFormat format = image.format();
        size_t bytes = 0;
        unsigned char *pixels = static_cast<unsigned char *>(image.write_to_memory(&bytes));
        int ok = pixels != nullptr;
        if (ok && format != VIPS_FORMAT_UCHAR && format != VIPS_FORMAT_USHORT) {
            std::fprintf(stderr, "harness: unexpected libvips band format %d\n", static_cast<int>(format));
            ok = 0;
        }
        if (ok) {
            result->width = static_cast<unsigned>(width);
            result->height = static_cast<unsigned>(height);
            vips_pixel(pixels, format, bands, 0, result->first);
            result->has_second = width > 1;
            if (result->has_second) vips_pixel(pixels, format, bands, 1, result->second);
        }
        g_free(pixels);
        return ok;
    } catch (const vips::VError &error) {
        std::fprintf(stderr, "libvips: %s\n", error.what());
        vips_error_clear();
        return 0;
    }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result;
    (void)parsarium_parse_png(data, size, &result);
    return 0;
}
