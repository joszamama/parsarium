#include <imago2.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int width = 0, height = 0;
    unsigned char *pixels = img_load_pixels(argv[1], &width, &height, IMG_FMT_RGBA32);
    if (!pixels || width < 2 || height < 1) return 3;
    printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           width, height, pixels[0], pixels[1], pixels[2], pixels[3],
           pixels[4], pixels[5], pixels[6], pixels[7]);
    img_free_pixels(pixels);
    return 0;
}
