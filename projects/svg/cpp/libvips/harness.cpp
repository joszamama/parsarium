#include "harness.h"
#include <vips/vips8>
#include <cstring>
#include <vector>
int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    if (VIPS_INIT("parsarium")) return 0;
    std::memset(result, 0, sizeof(*result));
    VipsBlob *blob = vips_blob_new(nullptr, data, size);
    if (!blob) return 0;
    int ok = 0;
    try {
        vips::VImage image = vips::VImage::svgload_buffer(blob);
        const int width = image.width(), height = image.height();
        if (width > 0 && height > 0) {
            auto first = image.getpoint(0, 0);
            /* The second sample is the next pixel in row-major order and is absent for a 1x1 image. */
            const bool second_present = width > 1 || height > 1;
            std::vector<double> second;
            if (second_present) second = image.getpoint(width > 1 ? 1 : 0, width > 1 ? 0 : 1);
            if (first.size() >= 3 && (!second_present || second.size() >= 3)) {
                result->width = static_cast<unsigned>(width);
                result->height = static_cast<unsigned>(height);
                result->second_present = second_present;
                for (int i = 0; i < 3; i++) {
                    result->first[i] = static_cast<unsigned char>(first[i]);
                    if (second_present) result->second[i] = static_cast<unsigned char>(second[i]);
                }
                ok = 1;
            }
        }
    } catch (const vips::VError &) {}
    vips_area_unref(VIPS_AREA(blob));
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_svg_result result;
    (void)parsarium_parse_svg(data, size, &result);
    return 0;
}
