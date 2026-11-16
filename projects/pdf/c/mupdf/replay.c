#include "harness.h"
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t *data = (uint8_t *)malloc(8u << 20);
    if (!data) { fclose(file); return 4; }
    size_t size = fread(data, 1, 8u << 20, file);
    if (ferror(file) || (size == (8u << 20) && fgetc(file) != EOF)) { free(data); fclose(file); return 4; }
    fclose(file);
    Result result;
    int ok = parse_data(data, size, &result);
    free(data);
    if (!ok) return 5;
    printf("{\"pages\":%d}\n", result.pages);
    return 0;
}
