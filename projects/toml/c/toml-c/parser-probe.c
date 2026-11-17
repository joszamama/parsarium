/* Parser-only probe: toml_parse on the local bytes, then free; no traversal or printing. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "toml.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 2;
    static char data[(1u << 20) + 1];
    size_t size = fread(data, 1, 1u << 20, file);
    fclose(file);
    if (size == 0 || size == 1u << 20 || memchr(data, 0, size)) return 2;
    data[size] = 0;
    char errbuf[200];
    toml_table_t *root = toml_parse(data, errbuf, sizeof errbuf);
    if (!root) return 1;
    toml_free(root);
    return 0;
}
