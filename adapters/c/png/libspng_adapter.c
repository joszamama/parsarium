#include "spng.h"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 1;
    spng_ctx *ctx = spng_ctx_new(0);
    if (!ctx) { fclose(file); return 1; }
    int error = spng_set_png_file(ctx, file);
    struct spng_ihdr header;
    size_t size = 0;
    if (!error) error = spng_get_ihdr(ctx, &header);
    if (!error) error = spng_decoded_image_size(ctx, SPNG_FMT_RGBA8, &size);
    unsigned char *pixels = error ? NULL : malloc(size);
    if (!error && !pixels) error = 1;
    if (!error) error = spng_decode_image(ctx, pixels, size, SPNG_FMT_RGBA8, 0);
    if (error) {
        fprintf(stderr, "libspng: %s\n", spng_strerror(error));
        free(pixels);
        spng_ctx_free(ctx);
        fclose(file);
        return 1;
    }
    if (size < 8) { free(pixels); spng_ctx_free(ctx); fclose(file); return 1; }
    printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           header.width, header.height, pixels[0], pixels[1], pixels[2], pixels[3],
           pixels[4], pixels[5], pixels[6], pixels[7]);
    free(pixels);
    spng_ctx_free(ctx);
    fclose(file);
    return 0;
}
