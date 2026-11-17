/* Parser-only probe: jv_parse_sized on the local bytes, then free; no printing. */
#include <stdint.h>
#include <stdio.h>

#include "jv.h"

/* jq seeds its object hash once per process from arc4random() (src/jv.c,
 * jvp_hash_seed_init) and documents no seed setting. Defining arc4random here
 * fixes that seed so object bucket layout, coverage and AFL++ feedback repeat;
 * parsing and the parsed value do not depend on it. */
uint32_t arc4random(void) { return 0x5eed5eedu; }

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 2;
    static char data[1u << 20];
    size_t size = fread(data, 1, sizeof data, file);
    fclose(file);
    if (size == 0 || size == sizeof data) return 2;
    jv root = jv_parse_sized(data, (int)size);
    int status = jv_is_valid(root) ? 0 : 1;
    jv_free(root);
    return status;
}
