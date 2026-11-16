#include "harness.h"
#include <gdk-pixbuf/gdk-pixbuf.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
int parsarium_parse_png(const uint8_t *data, size_t size, struct parsarium_png_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.png";
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
    int ok = gdk_pixbuf_get_width(image) == 2 && gdk_pixbuf_get_height(image) == 1 && channels == 4 && pixels;
    if (ok) {
        result->width = 2; result->height = 1;
        memcpy(result->first, pixels, 4); memcpy(result->second, pixels + 4, 4);
        result->has_second = 1;
    }
    g_object_unref(image);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result;
    (void)parsarium_parse_png(data, size, &result);
    return 0;
}
