#include "harness.h"
#include "lodepng.h"

#include <stdlib.h>
#include <string.h>

int parsarium_parse_png(const uint8_t *data, size_t size,
                        struct parsarium_png_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    unsigned char *pixels = NULL;
    unsigned width = 0, height = 0;
    unsigned error = lodepng_decode32(&pixels, &width, &height, data, size);
    if (error || width == 0 || height == 0 ||
        (uint64_t)width * height > (1u << 22)) {
        free(pixels);
        return 0;
    }
    result->width = width;
    result->height = height;
    memcpy(result->first, pixels, 4);
    result->has_second = (uint64_t)width * height > 1;
    if (result->has_second) memcpy(result->second, pixels + 4, 4);
    free(pixels);
    return 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result;
    (void)parsarium_parse_png(data, size, &result);
    return 0;
}
