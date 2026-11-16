#include "harness.h"
#include <vips/vips.h>
#include <string.h>
int parsarium_parse_pdf(const uint8_t *data, size_t size, struct parsarium_pdf_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    if (VIPS_INIT("parsarium")) return 0;
    memset(result, 0, sizeof(*result));
    VipsImage *image = NULL;
    if (vips_pdfload_buffer((void *)data, size, &image, NULL)) return 0;
    int pages = 0;
    int ok = !vips_image_get_int(image, "n-pages", &pages) && pages > 0 &&
             vips_image_get_width(image) > 0 && vips_image_get_height(image) > 0;
    if (ok) {
        result->pages = (unsigned)pages;
        result->width = (unsigned)vips_image_get_width(image);
        result->height = (unsigned)vips_image_get_height(image);
    }
    g_object_unref(image);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_pdf_result result;
    (void)parsarium_parse_pdf(data, size, &result);
    return 0;
}
