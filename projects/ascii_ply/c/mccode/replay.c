#include "harness.h"
#include <stdint.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t bytes[(1u << 20) + 1];
    size_t size = fread(bytes, 1, sizeof(bytes), file);
    if (ferror(file) || size > (1u << 20)) { fclose(file); return 4; }
    fclose(file);
    struct parsarium_ply_result result;
    if (!parsarium_parse_ply(bytes, size, &result)) return 5;
    printf("{\"vertices\":%ld,\"faces\":%ld,\"length\":%.6f,\"width\":%.6f}\n",
           result.vertices, result.faces, result.length, result.width);
    return 0;
}
