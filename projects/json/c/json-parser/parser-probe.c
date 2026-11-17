/* Parser-only probe: json_parse_ex on the local bytes, then free; no printing. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "json.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 2;
    static char data[1u << 20];
    size_t size = fread(data, 1, sizeof data, file);
    fclose(file);
    if (size == 0 || size == sizeof data) return 2;
    json_settings settings = {0};
    char error[json_error_max];
    json_value *root = json_parse_ex(&settings, data, size, error);
    if (!root) return 1;
    json_value_free(root);
    return 0;
}
