#include "harness.h"
#include <FreeImage.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
int parsarium_parse_ascii_pnm(const uint8_t *data, size_t size, struct parsarium_ascii_pnm_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.ppm";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    FreeImage_Initialise(0);
    FIBITMAP *image = FreeImage_Load(FIF_PPM, path, PNM_DEFAULT);
    unlink(path);
    int ok = image && FreeImage_GetWidth(image) == 2 && FreeImage_GetHeight(image) == 1;
    RGBQUAD first = {0}, second = {0};
    if (ok) ok = FreeImage_GetPixelColor(image, 0, 0, &first) && FreeImage_GetPixelColor(image, 1, 0, &second);
    if (ok) {
        result->width = 2; result->height = 1;
        RGBQUAD colors[2] = {first, second}; unsigned char *out[2] = {result->first, result->second};
        for (int i = 0; i < 2; i++) {
            out[i][0] = colors[i].rgbRed; out[i][1] = colors[i].rgbGreen;
            out[i][2] = colors[i].rgbBlue; out[i][3] = colors[i].rgbReserved;
        }
        result->has_second = 1;
    }
    if (image) FreeImage_Unload(image);
    FreeImage_DeInitialise();
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_ascii_pnm_result result; (void)parsarium_parse_ascii_pnm(data, size, &result); return 0;
}
