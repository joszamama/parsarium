#include "harness.h"

#include <cstdio>
#include <cstdint>

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
    parsarium_ply_result result;
    if (!parsarium_parse_ply(input, size, &result)) return 5;
    std::printf("{\"vertices\":%u,\"faces\":%zu,\"face\":[",
                result.vertices, result.faces);
    for (std::size_t i = 0; i < result.face.size(); ++i)
        std::printf("%s%u", i ? "," : "", result.face[i]);
    std::printf("]}\n");
    return 0;
}
