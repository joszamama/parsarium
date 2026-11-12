#define STBI_ONLY_PNG
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int width = 0, height = 0, channels = 0;
    unsigned char *pixels = stbi_load(argv[1], &width, &height, &channels, 4);
    if (!pixels) {
        fprintf(stderr, "stb_image: %s\n", stbi_failure_reason());
        return 1;
    }
    if (width < 2 || height < 1) { stbi_image_free(pixels); return 1; }
    printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           width, height, pixels[0], pixels[1], pixels[2], pixels[3],
           pixels[4], pixels[5], pixels[6], pixels[7]);
    stbi_image_free(pixels);
    return 0;
}
