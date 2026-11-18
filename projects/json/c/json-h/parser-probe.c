/* Parser-only probe: json_parse on the local bytes, then free; no printing.
 * json.h is header-only, so its functions are compiled into this file; the
 * AFL++ allowlist matches functions by their json.h debug location. */
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
#ifdef PARSARIUM_NO_PARSE
    return 0;
#else
    struct json_value_s *root = json_parse(data, size);
    if (!root) return 1;
    free(root);
    return 0;
#endif
}
