/* Parser-only probe: toml_parse on the local bytes, then free; no traversal or printing. */
#include <stdio.h>
#include <stdlib.h>

#include "tomlc17.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 2;
    static char data[1u << 20];
    size_t size = fread(data, 1, sizeof data, file);
    fclose(file);
    if (size == 0 || size == sizeof data) return 2;
    toml_result_t result = toml_parse(data, (int)size);
    int ok = result.ok;
    toml_free(result);
    return ok ? 0 : 1;
}
