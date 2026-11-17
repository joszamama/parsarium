#include "harness.h"
#include <gdk-pixbuf/gdk-pixbuf.h>
#include <string.h>

/* Rendering is bounded so a declared huge canvas cannot exhaust memory. */
#define PARSARIUM_MAX_PIXELS (4096u * 4096u)

static void copy_rgba(unsigned char output[4], const guchar *pixel, int channels) {
    memcpy(output, pixel, (size_t)channels);
    if (channels == 3) output[3] = 255;
}

static void size_prepared(GdkPixbufLoader *loader, int width, int height, gpointer data) {
    int *too_large = data;
    if (width <= 0 || height <= 0 || (guint64)width * (guint64)height > PARSARIUM_MAX_PIXELS) {
        *too_large = 1;
        gdk_pixbuf_loader_set_size(loader, 1, 1);
    }
}

int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    GdkPixbufLoader *loader = gdk_pixbuf_loader_new_with_type("svg", NULL);
    if (!loader) return 0;
    int too_large = 0;
    g_signal_connect(loader, "size-prepared", G_CALLBACK(size_prepared), &too_large);
    gboolean written = gdk_pixbuf_loader_write(loader, data, size, NULL);
    gboolean closed = gdk_pixbuf_loader_close(loader, NULL);
    GdkPixbufFormat *format = gdk_pixbuf_loader_get_format(loader);
    GdkPixbuf *image = gdk_pixbuf_loader_get_pixbuf(loader);
    int ok = written && closed && !too_large && format && image;
    if (ok) {
        gchar *name = gdk_pixbuf_format_get_name(format);
        ok = name && strcmp(name, "svg") == 0;
        g_free(name);
    }
    if (ok) {
        int width = gdk_pixbuf_get_width(image), height = gdk_pixbuf_get_height(image);
        int stride = gdk_pixbuf_get_rowstride(image);
        int channels = gdk_pixbuf_get_n_channels(image);
        const guchar *pixels = gdk_pixbuf_read_pixels(image);
        ok = pixels && width > 0 && height > 0 &&
             gdk_pixbuf_get_colorspace(image) == GDK_COLORSPACE_RGB &&
             (channels == 3 || channels == 4) && gdk_pixbuf_get_bits_per_sample(image) == 8;
        if (ok) {
            result->width = (unsigned)width;
            result->height = (unsigned)height;
            copy_rgba(result->first, pixels, channels);
            result->second_present = (guint64)width * (guint64)height > 1;
            if (result->second_present)
                copy_rgba(result->second, width > 1 ? pixels + channels : pixels + stride,
                          channels);
        }
    }
    g_object_unref(loader);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_svg_result result;
    (void)parsarium_parse_svg(data, size, &result);
    return 0;
}
