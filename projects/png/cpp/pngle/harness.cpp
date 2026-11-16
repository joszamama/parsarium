#include "harness.h"
#include "pngle.h"

#include <string.h>

struct pixel_capture {
    struct parsarium_png_result *result;
    unsigned seen;
};

static void capture(pngle_t *pngle, uint32_t x, uint32_t y, uint32_t w,
                    uint32_t h, const uint8_t rgba[4]) {
    struct pixel_capture *state = (struct pixel_capture *)pngle_get_user_data(pngle);
    if (y != 0 || w != 1 || h != 1 || x > 1) return;
    memcpy(x == 0 ? state->result->first : state->result->second, rgba, 4);
    state->seen |= 1u << x;
}

int parsarium_parse_png(const uint8_t *data, size_t size,
                        struct parsarium_png_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    pngle_t *decoder = pngle_new();
    if (!decoder) return 0;
    struct pixel_capture state = {result, 0};
    pngle_set_user_data(decoder, &state);
    pngle_set_draw_callback(decoder, capture);
    size_t offset = 0;
    while (offset < size) {
        int consumed = pngle_feed(decoder, (uint8_t *)data + offset, size - offset);
        if (consumed <= 0) { pngle_destroy(decoder); return 0; }
        offset += (size_t)consumed;
    }
    result->width = pngle_get_width(decoder);
    result->height = pngle_get_height(decoder);
    result->has_second = result->width > 1;
    int valid = result->width > 0 && result->height > 0 &&
                state.seen == (result->has_second ? 3u : 1u);
    pngle_destroy(decoder);
    return valid;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_png_result result;
    (void)parsarium_parse_png(data, size, &result);
    return 0;
}
