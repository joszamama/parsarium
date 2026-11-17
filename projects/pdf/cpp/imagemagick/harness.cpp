#include "harness.h"
#include <Magick++.h>
#include <cstring>
#include <exception>
#include <string>
#include <unistd.h>
#include <vector>

// Magick::readImages only forwards to MagickCore::ReadImage. ImageMagick is
// built with --with-gslib, so its PDF coder runs the linked Ghostscript
// library interpreter in this process instead of spawning gs.
int parse_data(const uint8_t *data, size_t size, Result *result) {
    static bool initialized;
    if (!data || !result || !size || size > (8u << 20)) return 0;
    std::memset(result, 0, sizeof(*result));
    if (!initialized) {
        Magick::InitializeMagick(nullptr);
        initialized = true;
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
    int ok = 0;
    try {
        std::vector<Magick::Image> pages;
        // The explicit PDF: prefix selects the PDF coder for every input.
        Magick::readImages(&pages, std::string("PDF:") + path);
        if (!pages.empty()) {
            result->pages = pages.size();
            result->width = pages[0].columns();
            result->height = pages[0].rows();
            ok = result->width > 0 && result->height > 0;
        }
    } catch (const std::exception &) {
    }
    unlink(path);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
