#include "harness.hpp"

#include <allheaders.h>
#include <string.h>

int parsarium_parse_pnm(const uint8_t *data, size_t size,
                        struct parsarium_pnm_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    PIX *image = pixReadMemPnm(data, size);
    if (!image) return 0;
    result->width = pixGetWidth(image);
    result->height = pixGetHeight(image);
    int ok = result->width >= 2 && result->height >= 1 &&
             result->width <= 4096 && result->height <= 4096 &&
             !pixGetRGBPixel(image, 0, 0, &result->first_rgb[0],
                              &result->first_rgb[1], &result->first_rgb[2]) &&
             !pixGetRGBPixel(image, 1, 0, &result->second_rgb[0],
                              &result->second_rgb[1], &result->second_rgb[2]);
    pixDestroy(&image);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_pnm_result result;
    (void)parsarium_parse_pnm(data, size, &result);
    return 0;
}
