#include "harness.hpp"

#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t input[1u << 20];
    size_t size = fread(input, 1, sizeof(input), file);
    if (ferror(file) || (size == sizeof(input) && fgetc(file) != EOF)) {
        fclose(file);
        return 4;
    }
    fclose(file);
    struct parsarium_pnm_result result;
    if (!parsarium_parse_pnm(input, size, &result)) return 5;
    printf("{\"width\":%d,\"height\":%d,\"first_rgb\":[%d,%d,%d],\"second_rgb\":[%d,%d,%d]}\n",
           result.width, result.height,
           result.first_rgb[0], result.first_rgb[1], result.first_rgb[2],
           result.second_rgb[0], result.second_rgb[1], result.second_rgb[2]);
    return 0;
}
