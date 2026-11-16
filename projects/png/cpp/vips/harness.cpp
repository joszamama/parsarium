#include "harness.h"
#include <vips/vips8>
#include <cstring>

int parsarium_parse_png(const uint8_t *data, size_t size, struct parsarium_png_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    if (VIPS_INIT("parsarium")) return 0;
    std::memset(result, 0, sizeof(*result));
    try {
        vips::VImage image = vips::VImage::new_from_buffer(data, size, "");
        int width = image.width(), height = image.height(), bands = image.bands();
        size_t bytes = 0;
        unsigned char *pixels = static_cast<unsigned char *>(image.write_to_memory(&bytes));
        int ok = pixels && width > 0 && height > 0 && bands == 4 &&
                 image.format() == VIPS_FORMAT_UCHAR &&
                 bytes >= static_cast<size_t>(width) * static_cast<size_t>(height) * static_cast<size_t>(bands);
        if (ok) {
            result->width = static_cast<unsigned>(width);
            result->height = static_cast<unsigned>(height);
            std::memcpy(result->first, pixels, 4);
            if (width * height > 1) std::memcpy(result->second, pixels + 4, 4);
        }
        g_free(pixels);
        return ok;
    } catch (const vips::VError &) {
        return 0;
    }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result;
    (void)parsarium_parse_png(data, size, &result);
    return 0;
}
