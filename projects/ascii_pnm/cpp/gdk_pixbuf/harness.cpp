#include "harness.h"
#include <gdk-pixbuf/gdk-pixbuf.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
int parsarium_parse_ascii_pnm(const uint8_t *data, size_t size, struct parsarium_ascii_pnm_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.ppm";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    GError *error = NULL;
    GdkPixbuf *image = gdk_pixbuf_new_from_file(path, &error);
    unlink(path);
    if (!image) { if (error) g_error_free(error); return 0; }
    int channels = gdk_pixbuf_get_n_channels(image);
    const guchar *pixels = gdk_pixbuf_read_pixels(image);
    int width = gdk_pixbuf_get_width(image), height = gdk_pixbuf_get_height(image);
    int ok = width > 0 && height > 0 && channels >= 3 && pixels;
    if (ok) {
        /* The second pixel is the next one in raster order, if the image has one. */
        const guchar *next = width > 1 ? pixels + channels
                             : height > 1 ? pixels + gdk_pixbuf_get_rowstride(image) : NULL;
        result->width = (unsigned)width; result->height = (unsigned)height;
        memcpy(result->first, pixels, 3);
        result->has_second = next != NULL;
        if (next) memcpy(result->second, next, 3);
    }
    g_object_unref(image);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_ascii_pnm_result result;
    (void)parsarium_parse_ascii_pnm(data, size, &result);
    return 0;
}
