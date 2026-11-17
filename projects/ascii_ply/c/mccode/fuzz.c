#include "harness.h"
#include <stdint.h>
#include <stdio.h>
#include <string.h>

/* One file per process: McCode's upstream parser exits on some invalid inputs. */
int main(int argc, char **argv) {
    if (argc != 2 || !strcmp(argv[1], "-help=1")) {
        puts("Usage: fuzzer PLY_FILE");
        return 0;
    }
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 2;
    uint8_t bytes[(1u << 20) + 1];
    size_t size = fread(bytes, 1, sizeof(bytes), file);
    if (ferror(file) || size > (1u << 20)) { fclose(file); return 3; }
    fclose(file);
    struct parsarium_ply_result result;
    (void)parsarium_parse_ply(bytes, size, &result);
    return 0;
}
