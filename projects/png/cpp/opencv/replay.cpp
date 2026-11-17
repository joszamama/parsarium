#include "harness.h"
#include <cstdio>
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    std::uint8_t data[1u << 20];
    std::size_t size = std::fread(data, 1, sizeof(data), file);
    if (std::ferror(file) || (size == sizeof(data) && std::fgetc(file) != EOF)) { std::fclose(file); return 4; }
    std::fclose(file);
    Result result{};
    if (!parse_data(data, size, &result)) return 5;
    const auto print_pixel = [](bool present, const std::uint8_t *rgba) {
        if (!present) { std::fputs("null", stdout); return; }
        std::printf("[%u,%u,%u,%u]", rgba[0], rgba[1], rgba[2], rgba[3]);
    };
    std::printf("{\"width\":%u,\"height\":%u,\"first\":", result.width, result.height);
    print_pixel(result.has_first, result.first);
    std::fputs(",\"second\":", stdout);
    print_pixel(result.has_second, result.second);
    std::fputs("}\n", stdout);
    return 0;
}
