#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "jv.h"

/* jq seeds its object hash once per process from arc4random() (src/jv.c,
 * jvp_hash_seed_init) and documents no seed setting. Defining arc4random here
 * fixes that seed so object bucket layout, coverage and AFL++ feedback repeat;
 * parsing and the parsed value do not depend on it. */
uint32_t arc4random(void) { return 0x5eed5eedu; }

/* jv_parse_sized parses exactly one JSON value from the given byte count. */
static jv parse_json(const uint8_t *data, size_t size) {
    if (!data || size == 0 || size > (1u << 20)) return jv_invalid();
    return jv_parse_sized((const char *)data, (int)size);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    jv_free(parse_json(data, size));
    return 0;
}

#ifndef PARSARIUM_FUZZER
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t *data = malloc((1u << 20) + 1);
    if (!data) { fclose(file); return 4; }
    size_t size = fread(data, 1, 1u << 20, file);
    if (ferror(file) || (size == (1u << 20) && fgetc(file) != EOF)) {
        free(data); fclose(file); return 4;
    }
    fclose(file);
    jv root = parse_json(data, size);
    free(data);
    if (!jv_is_valid(root)) { jv_free(root); return 5; }
    /* jq's own unsorted dump visits the jv tree in object insertion order and
     * prints each number from its preserved decimal literal. */
    jv text = jv_dump_string(root, 0);
    puts(jv_string_value(text));
    jv_free(text);
    return 0;
}
#endif
