#include "harness.h"
#include <gd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
static unsigned char alpha8(gdImagePtr image, int pixel) {
    int alpha7 = gdImageAlpha(image, pixel);
    return (unsigned char)(255u - (unsigned)((alpha7 * 255 + 63) / 127));
}
int parsarium_parse_png(const uint8_t *data, size_t size, struct parsarium_png_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.png";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    FILE *file = fopen(path, "rb");
    if (!file) { unlink(path); return 0; }
    gdImagePtr image = gdImageCreateFromPng(file);
    fclose(file); unlink(path);
    if (!image) return 0;
    int ok = gdImageSX(image) == 2 && gdImageSY(image) == 1;
    if (ok) {
        int pixels[2] = {gdImageGetPixel(image, 0, 0), gdImageGetPixel(image, 1, 0)};
        unsigned char *out[2] = {result->first, result->second};
        result->width = 2; result->height = 1;
        for (int i = 0; i < 2; i++) {
            out[i][0] = gdImageRed(image, pixels[i]); out[i][1] = gdImageGreen(image, pixels[i]);
            out[i][2] = gdImageBlue(image, pixels[i]); out[i][3] = alpha8(image, pixels[i]);
        }
        result->has_second = 1;
    }
    gdImageDestroy(image);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result; (void)parsarium_parse_png(data, size, &result); return 0;
}
