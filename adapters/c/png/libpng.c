#include <png.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    png_image image;
    memset(&image, 0, sizeof image);
    image.version = PNG_IMAGE_VERSION;
    if (!png_image_begin_read_from_file(&image, argv[1])) {
        fprintf(stderr, "libpng: %s\n", image.message);
        return 1;
    }
    image.format = PNG_FORMAT_RGBA;
    size_t size = PNG_IMAGE_SIZE(image);
    unsigned char *pixels = malloc(size);
    if (!pixels) return 1;
    if (!png_image_finish_read(&image, NULL, pixels, 0, NULL)) {
        fprintf(stderr, "libpng: %s\n", image.message);
        free(pixels);
        png_image_free(&image);
        return 1;
    }
    if (size < 8) { free(pixels); png_image_free(&image); return 1; }
    printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           image.width, image.height, pixels[0], pixels[1], pixels[2], pixels[3],
           pixels[4], pixels[5], pixels[6], pixels[7]);
    free(pixels);
    png_image_free(&image);
    return 0;
}
