#include "harness.h"
#include <vips/vips8>
#include <cstring>
int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    if (VIPS_INIT("parsarium")) return 0;
    std::memset(result, 0, sizeof(*result));
    VipsBlob *blob = vips_blob_new(nullptr, data, size);
    if (!blob) return 0;
    int ok = 0;
    try {
        vips::VImage image = vips::VImage::svgload_buffer(blob);
        auto first = image.getpoint(0, 0);
        auto second = image.getpoint(1, 0);
        if (image.width() > 1 && image.height() > 0 && first.size() >= 3 && second.size() >= 3) {
            result->width = static_cast<unsigned>(image.width());
            result->height = static_cast<unsigned>(image.height());
            for (int i = 0; i < 3; i++) {
                result->first[i] = static_cast<unsigned char>(first[i]);
                result->second[i] = static_cast<unsigned char>(second[i]);
            }
            ok = 1;
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
