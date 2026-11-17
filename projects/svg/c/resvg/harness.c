#define _GNU_SOURCE
#include "harness.h"
#include "resvg.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define PARSARIUM_MAX_INPUT (1u << 20)
#define PARSARIUM_MAX_PIXELS (4096u * 4096u)

int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result) {
    if (!data || !result || !size || size > PARSARIUM_MAX_INPUT) return 0;
    memset(result, 0, sizeof(*result));

    /* The selected C API takes a local SVG path, so materialize the supplied bytes. */
    char path[] = "/tmp/parsarium-resvg-XXXXXX.svg";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    if (close(fd)) { unlink(path); return 0; }

    resvg_options *options = resvg_options_create();
    if (!options) { unlink(path); return 0; }
    resvg_render_tree *tree = NULL;
    int32_t status = resvg_parse_tree_from_file(path, options, &tree);
    unlink(path);
    resvg_options_destroy(options);
    if (status != RESVG_OK || !tree) return 0;

    resvg_size dimensions = resvg_get_image_size(tree);
    int ok = isfinite(dimensions.width) && isfinite(dimensions.height) &&
             dimensions.width > 0 && dimensions.height > 0 &&
             dimensions.width <= 4096 && dimensions.height <= 4096;
    if (!ok) { resvg_tree_destroy(tree); return 0; }
    unsigned width = (unsigned)ceilf(dimensions.width);
    unsigned height = (unsigned)ceilf(dimensions.height);
    size_t pixels = (size_t)width * height;
    if (!width || !height || pixels > PARSARIUM_MAX_PIXELS) {
        resvg_tree_destroy(tree); return 0;
    }
    unsigned char *rgba = calloc(pixels, 4);
    if (!rgba) { resvg_tree_destroy(tree); return 0; }
    resvg_render(tree, resvg_transform_identity(), width, height, (char *)rgba);
    result->width = width;
    result->height = height;
    memcpy(result->first, rgba, 3);
    result->second_present = pixels > 1;
    if (result->second_present) memcpy(result->second, rgba + 4, 3);
    free(rgba);
    resvg_tree_destroy(tree);
    return 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_svg_result result;
    (void)parsarium_parse_svg(data, size, &result);
    return 0;
}
