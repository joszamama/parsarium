#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "yyjson.h"

static yyjson_doc *parse_json(const uint8_t *data, size_t size) {
    if (!data || size > (1u << 20)) return NULL;
    return yyjson_read((const char *)data, size, YYJSON_READ_NOFLAG);
}

#ifndef PARSARIUM_FUZZER
/* yyjson_read is yyjson_read_opts without an error report; the replay asks for
 * the report so a failed read prints yyjson's own message. */
static yyjson_doc *parse_json_reporting(const uint8_t *data, size_t size, yyjson_read_err *err) {
    if (!data || size > (1u << 20)) return NULL;
    return yyjson_read_opts((char *)data, size, YYJSON_READ_NOFLAG, NULL, err);
}
#endif

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    yyjson_doc *root = parse_json(data, size);
    if (root) {
        /* Printing visits the parser's value tree and checks it is usable. */
        char *text = yyjson_write(root, YYJSON_WRITE_NOFLAG, NULL);
        free(text);
        yyjson_doc_free(root);
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
    yyjson_read_err err = {0};
    yyjson_doc *root = parse_json_reporting(data, size, &err);
    free(data);
    if (!root) {
        if (err.msg) fprintf(stderr, "yyjson_read failed: %s (code %u, position %zu)\n", err.msg, err.code, err.pos);
        return 5;
    }
    char *text = yyjson_write(root, YYJSON_WRITE_NOFLAG, NULL);
    yyjson_doc_free(root);
    if (!text) return 6;
    puts(text);
    free(text);
    return 0;
}
#endif
