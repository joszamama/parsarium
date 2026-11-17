#include "harness.h"
#include <juce_graphics/juce_graphics.h>
#include <cmath>
#include <cstring>
#include <unistd.h>

static bool rounded(float value, long *out) {
    if (!std::isfinite(value) || std::fabs(value) > 1.0e9f) return false;
    *out = std::lround(value);
    return true;
}

int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    std::memset(result, 0, sizeof(*result));
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
    auto drawable = juce::Drawable::createFromSVGFile(juce::File(path));
    unlink(path);
    if (!drawable) return 0;
    const auto bounds = drawable->getDrawableBounds();
    return rounded(bounds.getWidth(), &result->width) && rounded(bounds.getHeight(), &result->height);
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_svg_result result;
    (void)parsarium_parse_svg(data, size, &result);
    return 0;
}
