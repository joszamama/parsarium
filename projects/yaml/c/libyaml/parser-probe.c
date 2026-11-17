/* Parser-only probe: yaml_parser_load on the local bytes, then free; no traversal or printing. */
#include <stdint.h>
#include <stdio.h>

#include "yaml.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 2;
    static unsigned char data[1u << 20];
    size_t size = fread(data, 1, sizeof data, file);
    fclose(file);
    if (size == 0 || size == sizeof data) return 2;
    yaml_parser_t parser;
    yaml_document_t document;
    if (!yaml_parser_initialize(&parser)) return 2;
    yaml_parser_set_input_string(&parser, data, size);
    int ok = yaml_parser_load(&parser, &document);
    if (ok) yaml_document_delete(&document);
    yaml_parser_delete(&parser);
    return ok ? 0 : 1;
}
