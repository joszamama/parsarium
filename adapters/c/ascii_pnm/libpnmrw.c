#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif
#include "libpnmrw.h"
#ifdef __cplusplus
}
#endif

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    pnm_init2(argv[0]);
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 1;
    int width = 0, height = 0, format = 0;
    xelval maxval = 0;
    xel **pixels = pnm_readpnm(file, &width, &height, &maxval, &format);
    fclose(file);
    if (!pixels || width != 2 || height != 1 || maxval != 255 || format != PPM_FORMAT) {
        if (pixels) pnm_freearray(pixels, height);
        return 1;
    }
    printf("{\"width\":%d,\"height\":%d,\"maxval\":%u,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
           width, height, maxval,
           PPM_GETR(pixels[0][0]), PPM_GETG(pixels[0][0]), PPM_GETB(pixels[0][0]),
           PPM_GETR(pixels[0][1]), PPM_GETG(pixels[0][1]), PPM_GETB(pixels[0][1]));
    pnm_freearray(pixels, height);
    return 0;
}
