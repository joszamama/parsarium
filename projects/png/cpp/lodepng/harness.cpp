#include "harness.hpp"

#include <lodepng.h>
#include <vector>

bool parsarium_parse_png(const std::uint8_t *data, std::size_t size,
                         ParsariumPngResult &result) {
    if (!data || size == 0 || size > (1u << 20)) return false;
    std::vector<unsigned char> pixels;
    unsigned width = 0, height = 0;
    if (lodepng::decode(pixels, width, height, data, size) != 0) return false;
    if (width < 2 || height == 0 ||
        static_cast<std::uint64_t>(width) * height > (1u << 22) || pixels.size() < 8)
        return false;
    result.width = width;
    result.height = height;
    for (unsigned i = 0; i < 4; i++) {
        result.first[i] = pixels[i];
        result.second[i] = pixels[i + 4];
    }
    return true;
}

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    ParsariumPngResult result{};
    (void)parsarium_parse_png(data, size, result);
    return 0;
}
