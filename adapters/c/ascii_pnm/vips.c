#include <vips/vips.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (VIPS_INIT(argv[0])) return 1;
    VipsImage *image = vips_image_new_from_file(argv[1], NULL);
    if (!image) { vips_shutdown(); return 1; }
    int width = vips_image_get_width(image), height = vips_image_get_height(image);
    int bands = vips_image_get_bands(image);
    size_t bytes = 0;
    void *memory = vips_image_write_to_memory(image, &bytes);
    if (width != 2 || height != 1 || bands != 3 || bytes < 6 || !memory ||
        vips_image_get_format(image) != VIPS_FORMAT_UCHAR) {
        if (memory) g_free(memory);
        g_object_unref(image);
        vips_shutdown();
        return 1;
    }
    const unsigned char *pixels = (const unsigned char *)memory;
    printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
           width, height, pixels[0], pixels[1], pixels[2],
           pixels[3], pixels[4], pixels[5]);
    g_free(memory);
    g_object_unref(image);
    vips_shutdown();
    return 0;
}
