#include "harness.h"
#include "mdal_c_compat.h"

#include <stdio.h>

/* MDAL's default logger writes to stdout; send its messages to stderr so the
 * JSON line stays alone on stdout and a failed load reports MDAL's reason. */
static int logged;

static void log_to_stderr(int level, int status, const char *message) {
    (void)level;
    logged = 1;
    fprintf(stderr, "MDAL status %d: %s\n", status, message ? message : "");
}

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
    MDAL_SetLoggerCallback(log_to_stderr);
    struct parsarium_ply_result result = {0};
    if (!parsarium_parse_ply(input, size, &result)) {
        if (!logged)
            fputs("MDAL_LoadMesh did not return a PLY mesh with a readable first face\n", stderr);
        return 5;
    }
    printf("{\"vertices\":%d,\"faces\":%d,\"indices\":[", result.vertices, result.faces);
    for (int i = 0; i < result.index_count; ++i)
        printf(i ? ",%d" : "%d", result.indices[i]);
    puts("]}");
    parsarium_free_result(&result);
    return 0;
}
