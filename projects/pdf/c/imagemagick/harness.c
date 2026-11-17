#include "harness.h"
#include <MagickWand/MagickWand.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

/* ImageMagick is built with --with-gslib, so its PDF coder runs the linked
   Ghostscript library interpreter in this process instead of spawning gs. */
int parse_data(const uint8_t *data, size_t size, Result *result) {
    static int initialized;
    if (!data || !result || !size || size > (8u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    if (!initialized) {
        MagickWandGenesis();
        initialized = 1;
    }
    char path[] = "/tmp/parsarium-XXXXXX.pdf";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    /* The explicit PDF: prefix selects the PDF coder for every input. */
    char filename[sizeof(path) + 4];
    snprintf(filename, sizeof(filename), "PDF:%s", path);
    int ok = 0;
    MagickWand *wand = NewMagickWand();
    if (wand && MagickReadImage(wand, filename) != MagickFalse) {
        size_t pages = MagickGetNumberImages(wand);
        if (pages > 0 && MagickSetIteratorIndex(wand, 0) != MagickFalse) {
            result->pages = pages;
            result->width = MagickGetImageWidth(wand);
            result->height = MagickGetImageHeight(wand);
            ok = result->width > 0 && result->height > 0;
        }
    }
    if (wand) DestroyMagickWand(wand);
    unlink(path);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
