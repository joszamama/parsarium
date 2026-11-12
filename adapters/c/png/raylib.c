#include <raylib.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    SetTraceLogLevel(LOG_NONE);
    Image image = LoadImage(argv[1]);
    if (!image.data || image.width != 2 || image.height != 1) {
        if (image.data) UnloadImage(image);
        return 1;
    }
    Color *pixels = LoadImageColors(image);
    if (!pixels) { UnloadImage(image); return 1; }
    printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           image.width, image.height, pixels[0].r, pixels[0].g, pixels[0].b, pixels[0].a,
           pixels[1].r, pixels[1].g, pixels[1].b, pixels[1].a);
    UnloadImageColors(pixels);
    UnloadImage(image);
    return 0;
}
