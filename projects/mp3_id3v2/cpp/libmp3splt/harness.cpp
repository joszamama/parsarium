#include "harness.h"
#ifdef __cplusplus
extern "C" {
#endif
#include <mp3splt.h>
#ifdef __cplusplus
}
#endif
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct output_state { size_t bytes; unsigned char first[4]; size_t first_length; };
static void on_write(const void *ptr, size_t size, size_t nmemb, void *ctx) {
    struct output_state *out = (struct output_state *)ctx;
    const unsigned char *chunk = (const unsigned char *)ptr;
    size_t length = size * nmemb;
    for (size_t i = 0; i < length && out->first_length < 4; ++i)
        out->first[out->first_length++] = chunk[i];
    out->bytes += length;
}
int parse_data(const uint8_t *data, size_t size, Result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.mp3";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    splt_code error = SPLT_OK;
    splt_state *state = mp3splt_new_state(&error);
    struct output_state out = {0, {0}, 0};
    int ok = 0;
    if (state && mp3splt_find_plugins(state) == SPLT_OK &&
        mp3splt_set_filename_to_split(state, path) == SPLT_OK &&
        mp3splt_set_int_option(state, SPLT_OPT_PRETEND_TO_SPLIT, SPLT_TRUE) == SPLT_OK &&
        mp3splt_set_pretend_to_split_write_function(state, on_write, &out) == SPLT_OK) {
        splt_point *start = mp3splt_point_new(0, &error);
        splt_point *end = mp3splt_point_new(50, &error);
        if (start && end && mp3splt_append_splitpoint(state, start) == SPLT_OK &&
            mp3splt_append_splitpoint(state, end) == SPLT_OK) {
            result->split_status = mp3splt_split(state);
            result->segment_bytes = out.bytes;
            memcpy(result->first, out.first, 4);
            ok = result->split_status == SPLT_OK_SPLIT && out.first_length == 4 && out.bytes > 0;
        }
    }
    if (state) mp3splt_free_state(state);
    unlink(path);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
