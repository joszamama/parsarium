#include "lodepng.h"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    unsigned char *pixels = NULL;
    unsigned width = 0, height = 0;
    unsigned error = lodepng_decode32_file(&pixels, &width, &height, argv[1]);
    if (error) {
        fprintf(stderr, "LodePNG: %s\n", lodepng_error_text(error));
        return 1;
    }
    if (width < 2 || height < 1) { free(pixels); return 1; }
    printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           width, height, pixels[0], pixels[1], pixels[2], pixels[3],
           pixels[4], pixels[5], pixels[6], pixels[7]);
    free(pixels);
    return 0;
}
