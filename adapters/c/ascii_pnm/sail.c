#include <sail/sail.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    struct sail_image *image = NULL;
    if (sail_load_from_file(argv[1], &image) != SAIL_OK || !image) return 3;
    if (image->pixel_format != SAIL_PIXEL_FORMAT_BPP24_RGB ||
        image->width != 2 || image->height != 1 || image->bytes_per_line < 6) {
        sail_destroy_image(image);
        return 4;
    }
    const unsigned char *pixels = image->pixels;
    printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
           image->width, image->height, pixels[0], pixels[1], pixels[2],
           pixels[3], pixels[4], pixels[5]);
    sail_destroy_image(image);
    return 0;
}
