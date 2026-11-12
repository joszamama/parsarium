#include <gd.h>
#include <stdio.h>

static unsigned alpha8(gdImagePtr image, int pixel) {
    int alpha7 = gdImageAlpha(image, pixel);
    return 255u - (unsigned) ((alpha7 * 255 + 63) / 127);
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 1;
    gdImagePtr image = gdImageCreateFromPng(file);
    fclose(file);
    if (!image) return 1;
    int width = gdImageSX(image), height = gdImageSY(image);
    if (width != 2 || height != 1) { gdImageDestroy(image); return 1; }
    int first = gdImageGetPixel(image, 0, 0), second = gdImageGetPixel(image, 1, 0);
    printf("{\"width\":%d,\"height\":%d,\"first\":[%d,%d,%d,%u],\"second\":[%d,%d,%d,%u]}\n",
           width, height, gdImageRed(image, first), gdImageGreen(image, first),
           gdImageBlue(image, first), alpha8(image, first),
           gdImageRed(image, second), gdImageGreen(image, second),
           gdImageBlue(image, second), alpha8(image, second));
    gdImageDestroy(image);
    return 0;
}
