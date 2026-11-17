#include "harness.h"
#include <cstdio>
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    static uint8_t bytes[1u << 20];
    const size_t size = std::fread(bytes, 1, sizeof(bytes), file);
    if (std::ferror(file) || (size == sizeof(bytes) && std::fgetc(file) != EOF)) { std::fclose(file); return 4; }
    std::fclose(file);
    struct parsarium_ascii_pnm_result result;
    if (!parsarium_parse_ascii_pnm(bytes, size, &result)) return 5;
    std::printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u,%u],\"second\":",
        result.width, result.height, result.first[0], result.first[1], result.first[2], result.first[3]);
    if (result.second_present)
        std::printf("[%u,%u,%u,%u]", result.second[0], result.second[1], result.second[2], result.second[3]);
    else
        std::fputs("null", stdout);
    std::puts("}");
    return 0;
}
