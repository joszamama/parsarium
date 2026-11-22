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
    struct parsarium_ply_result result;
    if (!parsarium_parse_ply(input, size, &result)) {
        const char *error = parsarium_last_error();
        if (error) fprintf(stderr, "SG_ObjectLoadPLY: %s\n", error);
        return 5;
    }
    printf("{\"vertices\":%u,\"faces\":%u,\"indices\":[", result.vertices, result.faces);
    for (unsigned i = 0; i < result.face_size; ++i)
        printf(i ? ",%d" : "%d", result.face[i]);
    puts("]}");
    return 0;
}
