#include <MagickWand/MagickWand.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    MagickWandGenesis();
    MagickWand *image = NewMagickWand();
    if (!image) return 1;
    if (MagickReadImage(image, argv[1]) == MagickFalse) {
        fprintf(stderr, "ImageMagick: read failed\n");
        image = DestroyMagickWand(image);
        MagickWandTerminus();
        return 1;
    }
    size_t width = MagickGetImageWidth(image), height = MagickGetImageHeight(image);
    unsigned char pixels[8] = {0};
    if (width != 2 || height != 1 ||
        MagickExportImagePixels(image, 0, 0, 2, 1, "RGBA", CharPixel, pixels) == MagickFalse) {
        image = DestroyMagickWand(image);
        MagickWandTerminus();
        return 1;
    }
    printf("{\"width\":%zu,\"height\":%zu,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           width, height, pixels[0], pixels[1], pixels[2], pixels[3],
           pixels[4], pixels[5], pixels[6], pixels[7]);
    image = DestroyMagickWand(image);
    MagickWandTerminus();
    return 0;
}
