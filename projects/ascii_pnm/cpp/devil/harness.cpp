#include "harness.h"
#include <IL/il.h>
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
    ilInit();
    ILuint image = 0; ilGenImages(1, &image); ilBindImage(image);
    int ok = ilLoadImage((const ILstring)path) && ilConvertImage(IL_RGBA, IL_UNSIGNED_BYTE);
    unlink(path);
    if (ok) ok = ilGetInteger(IL_IMAGE_WIDTH) == 2 && ilGetInteger(IL_IMAGE_HEIGHT) == 1;
    const unsigned char *pixels = ok ? ilGetData() : NULL;
    if (ok) ok = pixels != NULL;
    if (ok) {
        result->width = 2; result->height = 1;
        memcpy(result->first, pixels, 4); memcpy(result->second, pixels + 4, 4);
        result->has_second = 1;
    }
    ilDeleteImages(1, &image);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_ascii_pnm_result result; (void)parsarium_parse_ascii_pnm(data, size, &result); return 0;
}
