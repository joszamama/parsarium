#include "harness.h"

#define WUFFS_IMPLEMENTATION
#include "wuffs-v0.3.c"

#include <stdlib.h>

int parsarium_parse_png(const uint8_t *data, size_t size,
                        struct parsarium_png_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    wuffs_png__decoder *decoder = (wuffs_png__decoder *)wuffs_png__decoder__alloc();
    if (!decoder) return 0;
    wuffs_base__io_buffer input = wuffs_base__ptr_u8__reader((uint8_t *)data, size, true);
    wuffs_base__image_config config = wuffs_base__null_image_config();
    wuffs_base__status status = wuffs_png__decoder__decode_image_config(decoder, &config, &input);
    int valid = wuffs_base__status__is_ok(&status);
    if (valid) {
        result->width = wuffs_base__pixel_config__width(&config.pixcfg);
        result->height = wuffs_base__pixel_config__height(&config.pixcfg);
        valid = result->width > 0 && result->height > 0;
    }
    free(decoder);
    return valid;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result;
    (void)parsarium_parse_png(data, size, &result);
    return 0;
}
