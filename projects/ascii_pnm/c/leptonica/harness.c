#include "harness.h"

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
    /* The second pixel is the next one in raster order, if the image has one. */
    result->has_second = result->width > 1 || result->height > 1;
    int ok = result->width >= 1 && result->height >= 1 &&
             !pixGetRGBPixel(image, 0, 0, &result->first_rgb[0],
                              &result->first_rgb[1], &result->first_rgb[2]) &&
             (!result->has_second ||
              !pixGetRGBPixel(image, result->width > 1 ? 1 : 0, result->width > 1 ? 0 : 1,
                              &result->second_rgb[0], &result->second_rgb[1],
                              &result->second_rgb[2]));
    pixDestroy(&image);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_pnm_result result;
    (void)parsarium_parse_pnm(data, size, &result);
    return 0;
}
