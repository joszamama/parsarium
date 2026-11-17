#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "cJSON.h"

static cJSON *parse_json(const uint8_t *data, size_t size) {
    if (!data || size > (1u << 20)) return NULL;
    return cJSON_ParseWithLengthOpts((const char *)data, size, NULL, 0);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    cJSON *root = parse_json(data, size);
    if (root) {
        /* Printing visits the parser's value tree and checks it is usable. */
        char *text = cJSON_PrintUnformatted(root);
        cJSON_free(text);
        cJSON_Delete(root);
    }
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
    cJSON *root = parse_json(data, size);
    free(data);
    if (!root) return 5;
    char *text = cJSON_PrintUnformatted(root);
    cJSON_Delete(root);
    if (!text) return 6;
    puts(text);
    cJSON_free(text);
    return 0;
}
#endif
