#include "harness.h"
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
    struct parsarium_ply_result result = {0};
    if (!parsarium_parse_ply(input, size, &result)) {
        fprintf(stderr, "%s\n", result.error ? result.error : "parse failed");
        return 5;
    }
    printf("{\"meshes\":%u,\"vertices\":%u,\"faces\":%u,\"face\":[",
           result.meshes, result.vertices, result.faces);
    for (unsigned i = 0; i < result.face_count; ++i)
        printf(i ? ",%u" : "%u", result.face[i]);
    puts("]}");
    return 0;
}
