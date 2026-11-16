#include "harness.h"
#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t data[1u << 20];
    size_t size = std::fread(data, 1, sizeof(data), file);
    if (std::ferror(file) || (size == sizeof(data) && std::fgetc(file) != EOF)) {
        std::fclose(file);
        return 4;
    }
    std::fclose(file);
    parsarium_ply_result result;
    if (!parsarium_parse_ply(data, size, &result)) return 5;
    std::printf("{\"vertices\":%zu,\"faces\":%zu,\"face\":[%zu,%zu,%zu]}\n",
                result.vertices, result.faces, result.face[0], result.face[1], result.face[2]);
    return 0;
}
