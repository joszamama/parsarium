#include "harness.h"
#include <SFML/Graphics/Image.hpp>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

bool parse_data(const std::uint8_t *data, std::size_t size, Result *result) {
    if (!data || !result || !size || size > (1u << 20)) return false;
    std::memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.png";
    int fd = mkstemps(path, 4);
    if (fd < 0) return false;
    std::size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return false; }
        offset += static_cast<std::size_t>(n);
    }
    close(fd);
    sf::Image image;
    bool ok = image.loadFromFile(path);
    if (ok) {
        const auto size = image.getSize();
        if (size.x >= 2 && size.y >= 1) {
            const auto first = image.getPixel({0, 0});
            const auto second = image.getPixel({1, 0});
            result->width = size.x;
            result->height = size.y;
            result->first[0] = first.r; result->first[1] = first.g;
            result->first[2] = first.b; result->first[3] = first.a;
            result->second[0] = second.r; result->second[1] = second.g;
            result->second[2] = second.b; result->second[3] = second.a;
        } else ok = false;
    }
    unlink(path);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    Result result{};
    (void)parse_data(data, size, &result);
    return 0;
}
