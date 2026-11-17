#include "harness.h"
#include <gtk/gtk.h>

int parsarium_parse_svg(const uint8_t *data, size_t size,
                        struct parsarium_svg_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    static int initialized;
    if (!initialized) {
        gtk_init();
        initialized = 1;
    }

    GBytes *bytes = g_bytes_new(data, size);
    if (!bytes) return 0;
    GtkSvg *svg = gtk_svg_new_from_bytes(bytes);
    g_bytes_unref(bytes);
    if (!svg) return 0;

    GdkPaintable *paintable = GDK_PAINTABLE(svg);
    result->width = gdk_paintable_get_intrinsic_width(paintable);
    result->height = gdk_paintable_get_intrinsic_height(paintable);
    g_object_unref(svg);
    return result->width > 0 && result->height > 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_svg_result result;
    (void)parsarium_parse_svg(data, size, &result);
    return 0;
}
