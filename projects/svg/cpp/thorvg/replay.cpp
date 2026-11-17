#include "harness.h"

#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    static uint8_t input[1u << 20];
    size_t size = std::fread(input, 1, sizeof(input), file);
    if (std::ferror(file) || (size == sizeof(input) && std::fgetc(file) != EOF)) {
        std::fclose(file);
        return 4;
    }
    std::fclose(file);
    struct parsarium_svg_result result;
    if (!parsarium_parse_svg(input, size, &result)) return 5;
    std::printf("{\"width\":%u,\"height\":%u}\n", result.width, result.height);
    return 0;
}
