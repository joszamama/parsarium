#include "harness.h"
#include <plutosvg.h>
#include <plutovg.h>

int parsarium_parse_svg(const uint8_t *data, size_t size,
                        struct parsarium_svg_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    plutosvg_document_t *document = plutosvg_document_load_from_data(
        (const char *)data, (int)size, -1, -1, NULL, NULL);
    if (!document) return 0;
    plutovg_surface_t *surface = plutosvg_document_render_to_surface(
        document, NULL, -1, -1, NULL, NULL, NULL);
    int ok = 0;
    if (surface) {
        result->width = plutovg_surface_get_width(surface);
        result->height = plutovg_surface_get_height(surface);
        if (result->width == 2 && result->height == 1) {
            unsigned char rgba[8] = {0};
            plutovg_convert_argb_to_rgba(rgba, plutovg_surface_get_data(surface),
                                          2, 1, plutovg_surface_get_stride(surface));
            for (int i = 0; i < 3; i++) {
                result->first[i] = rgba[i];
                result->second[i] = rgba[i + 4];
            }
            ok = 1;
        }
        plutovg_surface_destroy(surface);
    }
    plutosvg_document_destroy(document);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_svg_result result;
    (void)parsarium_parse_svg(data, size, &result);
    return 0;
}
