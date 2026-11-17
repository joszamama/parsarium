/* Parser-only probe: strict fjson_tokener_parse_ex on the local bytes, then free; no printing. */
#include <stdio.h>

#include "json.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 2;
    static char data[1u << 20];
    size_t size = fread(data, 1, sizeof data, file);
    fclose(file);
    if (size == 0 || size == sizeof data) return 2;
    struct fjson_tokener *tok = fjson_tokener_new();
    if (!tok) return 2;
    fjson_tokener_set_flags(tok, FJSON_TOKENER_STRICT);
    struct fjson_object *root = fjson_tokener_parse_ex(tok, data, (int)size);
    int status = root && fjson_tokener_get_error(tok) == fjson_tokener_success ? 0 : 1;
    if (root) fjson_object_put(root);
    fjson_tokener_free(tok);
    return status;
}
