#include "harness.h"
#include <lunasvg.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.svg";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    auto document = lunasvg::Document::loadFromFile(path);
    unlink(path);
    if (!document) return 0;
    auto bitmap = document->renderToBitmap();
    if (bitmap.isNull() || bitmap.width() <= 0 || bitmap.height() <= 0) return 0;
    bitmap.convertToRGBA();
    const unsigned char *pixels = bitmap.data();
    if (!pixels) return 0;
    const int width = bitmap.width(), height = bitmap.height();
    result->width = unsigned(width); result->height = unsigned(height);
    memcpy(result->first, pixels, 3);
    /* The second sample is the next pixel in row-major order and is absent for a 1x1 bitmap. */
    result->second_present = width > 1 || height > 1;
    if (result->second_present)
        memcpy(result->second, width > 1 ? pixels + 4 : pixels + bitmap.stride(), 3);
    return 1;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_svg_result result; (void)parsarium_parse_svg(data, size, &result); return 0;
}
