#include <png.h>
#include "harness.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define PARSARIUM_MAX_INPUT (1u << 20)
#define PARSARIUM_MAX_PIXELS (1u << 22)

int parsarium_parse_png(const uint8_t *data, size_t size,
                        struct parsarium_png_result *result) {
    if (!data || !result || size == 0 || size > PARSARIUM_MAX_INPUT) return 0;
    memset(result, 0, sizeof(*result));
    png_image image;
    memset(&image, 0, sizeof(image));
    image.version = PNG_IMAGE_VERSION;
    if (!png_image_begin_read_from_memory(&image, data, size)) return 0;
    image.format = PNG_FORMAT_RGBA;
    if (!image.width || !image.height ||
        (uint64_t)image.width * image.height > PARSARIUM_MAX_PIXELS) {
        png_image_free(&image);
        return 0;
    }
    size_t bytes = PNG_IMAGE_SIZE(image);
    if (bytes < 4 || bytes > 4u * PARSARIUM_MAX_PIXELS) {
        png_image_free(&image);
        return 0;
    }
    unsigned char *pixels = (unsigned char *)malloc(bytes);
    if (!pixels) {
        png_image_free(&image);
        return 0;
    }
    int ok = png_image_finish_read(&image, NULL, pixels, 0, NULL);
    if (ok) {
        result->width = image.width;
        result->height = image.height;
        memcpy(result->first, pixels, 4);
        result->has_second = (uint64_t)image.width * image.height > 1;
        if (result->has_second) memcpy(result->second, pixels + 4, 4);
    }
    free(pixels);
    png_image_free(&image);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result;
    (void)parsarium_parse_png(data, size, &result);
    return 0;
}
