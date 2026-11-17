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
    std::printf("{\"points\":%zu,\"x_sum\":%.17g,\"y_sum\":%.17g,\"z_sum\":%.17g}\n",
                result.points, result.x_sum, result.y_sum, result.z_sum);
    return 0;
}
