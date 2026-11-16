#include "harness.h"
#include <stdio.h>
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb"); if (!file) return 3;
    uint8_t input[1u << 20]; size_t size = fread(input, 1, sizeof(input), file);
    if (ferror(file) || (size == sizeof(input) && fgetc(file) != EOF)) { fclose(file); return 4; }
    fclose(file);
    struct parsarium_pdf_result result;
    if (!parsarium_parse_pdf(input, size, &result)) return 5;
    printf("{\"pages\":%u,\"width\":%u,\"height\":%u}\n", result.pages,result.width,result.height);
    return 0;
}
