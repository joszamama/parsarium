#include "harness.h"
#include <allheaders.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
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
    PIX *image = pixRead(path);
    unlink(path);
    if (!image) return 0;
    int ok = pixGetWidth(image) == 2 && pixGetHeight(image) == 1;
    int rgb[6] = {0};
    if (ok) ok = pixGetRGBPixel(image, 0, 0, &rgb[0], &rgb[1], &rgb[2]) == 0 &&
                 pixGetRGBPixel(image, 1, 0, &rgb[3], &rgb[4], &rgb[5]) == 0;
    if (ok) {
        result->width = 2; result->height = 1;
        for (int i = 0; i < 3; i++) { result->first[i] = (unsigned char)rgb[i]; result->second[i] = (unsigned char)rgb[i+3]; }
    }
    pixDestroy(&image);
    return ok;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result; (void)parsarium_parse_png(data, size, &result); return 0;
}
