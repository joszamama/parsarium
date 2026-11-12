#include <wand/wand_api.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    InitializeMagick(argv[0]);
    MagickWand *image = NewMagickWand();
    if (!image) return 1;
    if (MagickReadImage(image, argv[1]) == MagickFalse) {
        DestroyMagickWand(image); return 1;
    }
    unsigned long width = MagickGetImageWidth(image), height = MagickGetImageHeight(image);
    unsigned char pixels[8] = {0};
    if (width != 2 || height != 1 ||
        MagickGetImagePixels(image, 0, 0, 2, 1, "RGBA", CharPixel, pixels) == MagickFalse) {
        DestroyMagickWand(image); return 1;
    }
    printf("{\"width\":%lu,\"height\":%lu,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           width, height, pixels[0], pixels[1], pixels[2], pixels[3],
           pixels[4], pixels[5], pixels[6], pixels[7]);
    DestroyMagickWand(image);
    return 0;
}
