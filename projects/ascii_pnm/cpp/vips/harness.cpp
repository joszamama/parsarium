#include "harness.h"
#include <vips/vips8>
#include <cstring>

int parsarium_parse_pnm(const uint8_t *data, size_t size, struct parsarium_pnm_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    if (VIPS_INIT("parsarium")) return 0;
    std::memset(result, 0, sizeof(*result));
    try {
        vips::VImage image = vips::VImage::new_from_buffer(data, size, "");
        int width = image.width(), height = image.height(), bands = image.bands();
        size_t bytes = 0;
        unsigned char *pixels = static_cast<unsigned char *>(image.write_to_memory(&bytes));
        // 8-bit samples for maxval up to 255, 16-bit above. The second pixel
        // is the next one in raster order, if the image has one.
        VipsBandFormat format = image.format();
        size_t sample = format == VIPS_FORMAT_USHORT ? 2 : 1;
        int ok = pixels && width > 0 && height > 0 && bands == 3 &&
                 (format == VIPS_FORMAT_UCHAR || format == VIPS_FORMAT_USHORT) &&
                 bytes >= static_cast<size_t>(width) * static_cast<size_t>(height) *
                              static_cast<size_t>(bands) * sample;
        if (ok) {
            const unsigned short *wide = reinterpret_cast<const unsigned short *>(pixels);
            result->width = static_cast<unsigned>(width);
            result->height = static_cast<unsigned>(height);
            result->has_second = static_cast<size_t>(width) * static_cast<size_t>(height) > 1;
            for (int c = 0; c < 3; ++c) {
                result->first[c] = sample == 2 ? wide[c] : pixels[c];
                if (result->has_second) result->second[c] = sample == 2 ? wide[3 + c] : pixels[3 + c];
            }
        }
        g_free(pixels);
        return ok;
    } catch (const vips::VError &) {
        return 0;
    }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_pnm_result result;
    (void)parsarium_parse_pnm(data, size, &result);
    return 0;
}
