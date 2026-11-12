#include <FreeImage.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FreeImage_Initialise(0);
    FIBITMAP *image = FreeImage_Load(FIF_PPM, argv[1], PNM_DEFAULT);
    if (!image) { FreeImage_DeInitialise(); return 1; }
    unsigned width = FreeImage_GetWidth(image), height = FreeImage_GetHeight(image);
    RGBQUAD first, second;
    if (width != 2 || height != 1 ||
        !FreeImage_GetPixelColor(image, 0, 0, &first) ||
        !FreeImage_GetPixelColor(image, 1, 0, &second)) {
        FreeImage_Unload(image); FreeImage_DeInitialise(); return 1;
    }
    printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
           width, height, first.rgbRed, first.rgbGreen, first.rgbBlue,
           second.rgbRed, second.rgbGreen, second.rgbBlue);
    FreeImage_Unload(image);
    FreeImage_DeInitialise();
    return 0;
}
