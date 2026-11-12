#include <gdk-pixbuf/gdk-pixbuf.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    GError *error = NULL;
    GdkPixbuf *image = gdk_pixbuf_new_from_file(argv[1], &error);
    if (!image) {
        fprintf(stderr, "gdk-pixbuf: %s\n", error ? error->message : "load failed");
        if (error) g_error_free(error);
        return 1;
    }
    int width = gdk_pixbuf_get_width(image), height = gdk_pixbuf_get_height(image);
    int channels = gdk_pixbuf_get_n_channels(image);
    if (width != 2 || height != 1 || channels != 3) { g_object_unref(image); return 1; }
    const guchar *pixels = gdk_pixbuf_read_pixels(image);
    printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
           width, height, pixels[0], pixels[1], pixels[2],
           pixels[3], pixels[4], pixels[5]);
    g_object_unref(image);
    return 0;
}
