#include "harness.h"
#include <Imlib2.h>
#include <stdlib.h>
#include <string.h>
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
    Imlib_Image image = imlib_load_image_immediately(path);
    unlink(path);
    if (!image) return 0;
    imlib_context_set_image(image);
    int width = imlib_image_get_width(), height = imlib_image_get_height();
    const uint32_t *pixels = imlib_image_get_data_for_reading_only();
    int ok = width == 2 && height == 1 && pixels;
    if (ok) {
        result->width = (unsigned)width; result->height = (unsigned)height;
        const uint32_t first = pixels[0], second = pixels[1];
        const uint32_t values[2] = {first, second};
        unsigned char *out[2] = {result->first, result->second};
        for (int i = 0; i < 2; i++) {
            out[i][0] = (values[i] >> 16) & 255;
            out[i][1] = (values[i] >> 8) & 255;
            out[i][2] = values[i] & 255;
            out[i][3] = values[i] >> 24;
        }
        result->has_second = 1;
    }
    imlib_free_image();
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result;
    (void)parsarium_parse_png(data, size, &result);
    return 0;
}
