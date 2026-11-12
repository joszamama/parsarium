#include <allheaders.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    PIX *image = pixRead(argv[1]);
    if (!image) return 1;
    int width = pixGetWidth(image), height = pixGetHeight(image);
    int r0, g0, b0, r1, g1, b1;
    if (width != 2 || height != 1 ||
        pixGetRGBPixel(image, 0, 0, &r0, &g0, &b0) ||
        pixGetRGBPixel(image, 1, 0, &r1, &g1, &b1)) {
        pixDestroy(&image); return 1;
    }
    printf("{\"width\":%d,\"height\":%d,\"first_rgb\":[%d,%d,%d],\"second_rgb\":[%d,%d,%d]}\n",
           width, height, r0, g0, b0, r1, g1, b1);
    pixDestroy(&image);
    return 0;
}
