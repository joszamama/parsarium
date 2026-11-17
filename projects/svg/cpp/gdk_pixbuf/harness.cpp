#include "harness.h"
#include <gdk-pixbuf/gdk-pixbuf.h>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

#define PARSARIUM_MAX_PIXELS (4096u * 4096u)

static void copy_rgba(unsigned char output[4], const guchar *pixel, int channels) {
    std::memcpy(output, pixel, static_cast<size_t>(channels));
    if (channels == 3) output[3] = 255;
}

int parsarium_parse_svg(const uint8_t *bytes, size_t size, struct parsarium_svg_result *result) {
    if (!bytes || !result || !size || size > (1u << 20)) return 0;
    std::memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.svg";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t written = write(fd, bytes + offset, size - offset);
        if (written <= 0) { close(fd); unlink(path); return 0; }
        offset += static_cast<size_t>(written);
    }
    close(fd);

    int identified_width = 0, identified_height = 0;
    GdkPixbufFormat *format = gdk_pixbuf_get_file_info(path, &identified_width,
                                                        &identified_height);
    gchar *name = format ? gdk_pixbuf_format_get_name(format) : nullptr;
    bool svg = name && std::strcmp(name, "svg") == 0;
    g_free(name);
    if (!svg || identified_width <= 0 || identified_height <= 0 ||
        static_cast<guint64>(identified_width) * identified_height > PARSARIUM_MAX_PIXELS) {
        unlink(path);
        return 0;
    }

    GError *error = nullptr;
    GdkPixbuf *image = gdk_pixbuf_new_from_file(path, &error);
    unlink(path);
    if (error) g_error_free(error);
    if (!image) return 0;
    int width = gdk_pixbuf_get_width(image), height = gdk_pixbuf_get_height(image);
    int channels = gdk_pixbuf_get_n_channels(image);
    int stride = gdk_pixbuf_get_rowstride(image);
    const guchar *pixels = gdk_pixbuf_read_pixels(image);
    bool ok = pixels && width > 0 && height > 0 &&
              static_cast<guint64>(width) * height <= PARSARIUM_MAX_PIXELS &&
              gdk_pixbuf_get_colorspace(image) == GDK_COLORSPACE_RGB &&
              (channels == 3 || channels == 4) &&
              gdk_pixbuf_get_bits_per_sample(image) == 8;
    if (ok) {
        result->width = static_cast<unsigned>(width);
        result->height = static_cast<unsigned>(height);
        copy_rgba(result->first, pixels, channels);
        result->second_present = static_cast<guint64>(width) * height > 1;
        if (result->second_present)
            copy_rgba(result->second, width > 1 ? pixels + channels : pixels + stride,
                      channels);
    }
    g_object_unref(image);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *bytes, size_t size) {
    struct parsarium_svg_result result;
    (void)parsarium_parse_svg(bytes, size, &result);
    return 0;
}
