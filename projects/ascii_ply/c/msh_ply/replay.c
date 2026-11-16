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
    struct parsarium_ply_result result;
    if (!parsarium_parse_ply(data, size, &result)) return 5;
    printf("{\"vertices\":%d,\"faces\":%d,\"second_x\":%.1f,\"last_index\":%d}\n",
           result.vertices, result.faces, result.second_x, result.last_index);
    return 0;
}
