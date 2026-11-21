#include "harness.h"
#include <stdio.h>
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t input[1u << 20];
    size_t size = fread(input, 1, sizeof(input), file);
    if (ferror(file) || (size == sizeof(input) && fgetc(file) != EOF)) { fclose(file); return 4; }
    fclose(file);
    struct parsarium_pnm_result result;
    if (!parsarium_parse_pnm(input, size, &result)) return 5;
    printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u],\"second\":",
           result.width, result.height, result.first[0], result.first[1], result.first[2]);
    if (result.has_second) printf("[%u,%u,%u]}\n", result.second[0], result.second[1], result.second[2]);
    else printf("null}\n");
    return 0;
}
