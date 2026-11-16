#include "harness.h"

#define STB_IMAGE_IMPLEMENTATION
#define STBI_ONLY_PNG
#define STBI_MAX_DIMENSIONS 2048
#include "stb_image.h"

#include <stdlib.h>
#include <string.h>

int parsarium_parse_png(const uint8_t *data, size_t size,
                        struct parsarium_png_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    int width = 0, height = 0, source_channels = 0;
    stbi_uc *pixels = stbi_load_from_memory(data, (int)size, &width, &height,
                                            &source_channels, 4);
    if (!pixels) return 0;
    if (width <= 0 || height <= 0 || width > 2048 || height > 2048) {
        stbi_image_free(pixels);
        return 0;
    }
    result->width = (unsigned)width;
    result->height = (unsigned)height;
    memcpy(result->first, pixels, 4);
    result->has_second = (uint64_t)width * height > 1;
    if (result->has_second) memcpy(result->second, pixels + 4, 4);
    stbi_image_free(pixels);
    return 1;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result;
    (void)parsarium_parse_png(data, size, &result);
    return 0;
}
