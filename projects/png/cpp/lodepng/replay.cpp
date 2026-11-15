#include "harness.hpp"

#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    std::uint8_t input[1u << 20];
    std::size_t size = std::fread(input, 1, sizeof(input), file);
    if (std::ferror(file) || (size == sizeof(input) && std::fgetc(file) != EOF)) {
        std::fclose(file);
        return 4;
    }
    std::fclose(file);
    ParsariumPngResult result{};
    if (!parsarium_parse_png(input, size, result)) return 5;
    std::printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
                result.width, result.height,
                result.first[0], result.first[1], result.first[2], result.first[3],
                result.second[0], result.second[1], result.second[2], result.second[3]);
    return 0;
}
