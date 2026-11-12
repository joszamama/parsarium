#include <netpbm/ppm.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 1;
    int width = 0, height = 0;
    pixval maxval = 0;
    pixel **pixels = ppm_readppm(file, &width, &height, &maxval);
    fclose(file);
    if (!pixels || width != 2 || height != 1 || maxval != 255) {
        if (pixels) ppm_freearray(pixels, height);
        return 1;
    }
    printf("{\"width\":%d,\"height\":%d,\"maxval\":%u,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
           width, height, maxval,
           PPM_GETR(pixels[0][0]), PPM_GETG(pixels[0][0]), PPM_GETB(pixels[0][0]),
           PPM_GETR(pixels[0][1]), PPM_GETG(pixels[0][1]), PPM_GETB(pixels[0][1]));
    ppm_freearray(pixels, height);
    return 0;
}
