#include "harness.h"
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t data[1u << 20];
    size_t size = fread(data, 1, sizeof(data), file);
    if (ferror(file) || (size == sizeof(data) && fgetc(file) != EOF)) {
        fclose(file); return 4;
    }
    fclose(file);
    struct parsarium_pnm_result result;
    if (!parsarium_parse_pnm(data, size, &result)) return 5;
    printf("{\"width\":%zu,\"height\":%zu,\"maxval\":%u,"
           "\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
           result.width, result.height, result.maxval,
           result.first[0], result.first[1], result.first[2],
           result.second[0], result.second[1], result.second[2]);
    return 0;
}
