#include <Imlib2.h>
#include <stdint.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    Imlib_Image image = imlib_load_image_immediately(argv[1]);
    if (!image) return 1;
    imlib_context_set_image(image);
    int width = imlib_image_get_width(), height = imlib_image_get_height();
    const uint32_t *pixels = imlib_image_get_data_for_reading_only();
    if (width != 2 || height != 1 || !pixels) { imlib_free_image(); return 1; }
    uint32_t first = pixels[0], second = pixels[1];
    printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           width, height, (first >> 16) & 255, (first >> 8) & 255, first & 255, first >> 24,
           (second >> 16) & 255, (second >> 8) & 255, second & 255, second >> 24);
    imlib_free_image();
    return 0;
}
