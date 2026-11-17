#include "harness.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* BRL-CAD's PLY callback retains a vertex index across parses.  Keep each
 * input in a fresh process so the pinned importer is exercised unchanged. */
int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "-help=1") == 0) {
        puts("Usage: fuzzer LOCAL_PLY_FILE (one input per process)");
        return 0;
    }
    if (argc != 2) {
        fputs("Usage: fuzzer LOCAL_PLY_FILE (one input per process)\n", stderr);
        return 2;
    }
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t *input = (uint8_t *)malloc(1u << 20);
    if (!input) { fclose(file); return 4; }
    size_t size = fread(input, 1, 1u << 20, file);
    if (ferror(file) || (size == (1u << 20) && fgetc(file) != EOF)) {
        free(input);
        fclose(file);
        return 4;
    }
    fclose(file);
    struct parsarium_ply_result result = {0};
    int parsed = parsarium_parse_ply(input, size, &result);
    free(input);
    if (parsed) {
        printf("{\"parsed\":true,\"vertices\":%zu,\"faces\":%zu,\"second_x\":%.17g,\"face\":[%d,%d,%d]}\n",
               result.vertices, result.faces, result.second_x,
               result.face[0], result.face[1], result.face[2]);
    } else {
        puts("{\"parsed\":false}");
    }
    return 0;
}
