#include "harness.h"
#include <vips/vips8>
#include <cstring>
int parsarium_parse_pdf(const uint8_t *data, size_t size, struct parsarium_pdf_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    if (VIPS_INIT("parsarium")) return 0;
    std::memset(result, 0, sizeof(*result));
    VipsBlob *blob = vips_blob_new(nullptr, data, size);
    if (!blob) return 0;
    int ok = 0;
    try {
        vips::VImage image = vips::VImage::pdfload_buffer(blob);
        int pages = image.get_int("n-pages");
        if (pages > 0 && image.width() > 0 && image.height() > 0) {
            result->pages = static_cast<unsigned>(pages);
            result->width = static_cast<unsigned>(image.width());
            result->height = static_cast<unsigned>(image.height());
            ok = 1;
        }
    } catch (const vips::VError &) {}
    vips_area_unref(VIPS_AREA(blob));
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_pdf_result result;
    (void)parsarium_parse_pdf(data, size, &result);
    return 0;
}
