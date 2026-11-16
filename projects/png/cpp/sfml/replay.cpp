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
    std::printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
                result.width, result.height, result.first[0], result.first[1], result.first[2], result.first[3],
                result.second[0], result.second[1], result.second[2], result.second[3]);
    return 0;
}
