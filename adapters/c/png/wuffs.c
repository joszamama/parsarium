#include <stdio.h>
#include <stdlib.h>

#define WUFFS_IMPLEMENTATION
#include "wuffs-v0.3.c"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 1;
    if (fseek(file, 0, SEEK_END) != 0) { fclose(file); return 1; }
    long size = ftell(file);
    if (size <= 0 || fseek(file, 0, SEEK_SET) != 0) { fclose(file); return 1; }
    uint8_t *bytes = malloc((size_t) size);
    if (!bytes || fread(bytes, 1, (size_t) size, file) != (size_t) size) {
        free(bytes); fclose(file); return 1;
    }
    fclose(file);
    wuffs_png__decoder *decoder = wuffs_png__decoder__alloc();
    if (!decoder) { free(bytes); return 1; }
    wuffs_base__io_buffer input = wuffs_base__ptr_u8__reader(bytes, (size_t) size, true);
    wuffs_base__image_config config = wuffs_base__null_image_config();
    wuffs_base__status status = wuffs_png__decoder__decode_image_config(decoder, &config, &input);
    if (!wuffs_base__status__is_ok(&status)) {
        fprintf(stderr, "Wuffs PNG: %s\n", status.repr);
        free(decoder); free(bytes); return 1;
    }
    unsigned width = wuffs_base__pixel_config__width(&config.pixcfg);
    unsigned height = wuffs_base__pixel_config__height(&config.pixcfg);
    printf("{\"width\":%u,\"height\":%u}\n", width, height);
    free(decoder);
    free(bytes);
    return 0;
}
