#include "harness.h"

#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    static std::uint8_t input[1u << 20];
    std::size_t size = std::fread(input, 1, sizeof(input), file);
    if (std::ferror(file) || (size == sizeof(input) && std::fgetc(file) != EOF)) {
        std::fclose(file);
        return 4;
    }
    std::fclose(file);
    parsarium_svg_result result{};
    if (!parsarium_parse_svg(input, size, &result)) return 5;
    std::printf("{\"width\":%d,\"height\":%d,\"left_rgb\":[%u,%u,%u],\"right_rgb\":",
                result.width, result.height, result.first[0], result.first[1],
                result.first[2]);
    if (result.second_present)
        std::printf("[%u,%u,%u]}", result.second[0], result.second[1], result.second[2]);
    else
        std::printf("null}");
    std::putchar('\n');
    return 0;
}
