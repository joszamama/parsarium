#include <IL/il.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    ilInit();
    ILuint image = 0;
    ilGenImages(1, &image);
    ilBindImage(image);
    if (!ilLoadImage((const ILstring) argv[1]) ||
        !ilConvertImage(IL_RGBA, IL_UNSIGNED_BYTE)) {
        ilDeleteImages(1, &image); return 1;
    }
    int width = ilGetInteger(IL_IMAGE_WIDTH), height = ilGetInteger(IL_IMAGE_HEIGHT);
    const unsigned char *pixels = ilGetData();
    if (width != 2 || height != 1 || !pixels) { ilDeleteImages(1, &image); return 1; }
    printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           width, height, pixels[0], pixels[1], pixels[2], pixels[3],
           pixels[4], pixels[5], pixels[6], pixels[7]);
    ilDeleteImages(1, &image);
    return 0;
}
