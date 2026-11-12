#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "pngle.h"

struct pixels {
    uint8_t values[8];
    unsigned drawn;
};

static void on_draw(pngle_t *pngle, uint32_t x, uint32_t y, uint32_t w,
                    uint32_t h, const uint8_t rgba[4]) {
    struct pixels *result = pngle_get_user_data(pngle);
    if (x < 2 && y == 0 && w == 1 && h == 1) {
        for (int channel = 0; channel < 4; channel++)
            result->values[x * 4 + channel] = rgba[channel];
        result->drawn |= 1u << x;
    }
}

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
    pngle_t *pngle = pngle_new();
    if (!pngle) { free(bytes); return 1; }
    struct pixels result = {{0}, 0};
    pngle_set_user_data(pngle, &result);
    pngle_set_draw_callback(pngle, on_draw);
    size_t offset = 0;
    while (offset < (size_t) size) {
        int consumed = pngle_feed(pngle, bytes + offset, (size_t) size - offset);
        if (consumed <= 0) {
            fprintf(stderr, "pngle: %s\n", pngle_error(pngle));
            pngle_destroy(pngle); free(bytes); return 1;
        }
        offset += (size_t) consumed;
    }
    unsigned width = pngle_get_width(pngle), height = pngle_get_height(pngle);
    if (width != 2 || height != 1 || result.drawn != 3) {
        pngle_destroy(pngle); free(bytes); return 1;
    }
    printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           width, height, result.values[0], result.values[1], result.values[2], result.values[3],
           result.values[4], result.values[5], result.values[6], result.values[7]);
    pngle_destroy(pngle);
    free(bytes);
    return 0;
}
