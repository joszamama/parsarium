#include "harness.h"
#include "spng.h"

#include <stdlib.h>
#include <string.h>

int parsarium_parse_png(const uint8_t *data, size_t length,
                        struct parsarium_png_result *result) {
    if (!data || !result || length == 0 || length > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    spng_ctx *ctx = spng_ctx_new(0);
    if (!ctx) return 0;
    struct spng_ihdr header;
    size_t size = 0;
    int error = spng_set_png_buffer(ctx, (void *)data, length);
    if (!error) error = spng_get_ihdr(ctx, &header);
    if (!error && (header.width == 0 || header.height == 0 ||
                   (uint64_t)header.width * header.height > (1u << 22))) error = 1;
    if (!error) error = spng_decoded_image_size(ctx, SPNG_FMT_RGBA8, &size);
    unsigned char *pixels = error ? NULL : malloc(size);
    if (!error && !pixels) error = 1;
    if (!error) error = spng_decode_image(ctx, pixels, size, SPNG_FMT_RGBA8, 0);
    if (!error && size < 4) error = 1;
    if (!error) {
        result->width = header.width;
        result->height = header.height;
        memcpy(result->first, pixels, 4);
        result->has_second = (uint64_t)header.width * header.height > 1 && size >= 8;
        if (result->has_second) memcpy(result->second, pixels + 4, 4);
    }
    free(pixels);
    spng_ctx_free(ctx);
    return !error;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result;
    (void)parsarium_parse_png(data, size, &result);
    return 0;
}
