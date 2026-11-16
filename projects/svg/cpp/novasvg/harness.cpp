#include "harness.h"
#include <novasvg/novasvg.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.svg";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    auto document = novasvg::Document::loadFromFile(path);
    unlink(path);
    if (!document) return 0;
    result->width = (unsigned)document->width(); result->height = (unsigned)document->height();
    result->rectangles = (unsigned)document->querySelectorAll("rect").size();
    return result->width == 2 && result->height == 1 && result->rectangles == 2;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_svg_result result; (void)parsarium_parse_svg(data, size, &result); return 0;
}
