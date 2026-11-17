/* libyaml document API over local bytes: yaml_parser_set_input_string + yaml_parser_load.
 * The replay prints the loaded document graph as a typed tree (aliases expanded by
 * following libyaml's shared node indexes); see typed.h for the adapter-side typing. */
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "yaml.h"
#include "typed.h"

#define MAX_INPUT (1u << 20)
#define MAX_DEPTH 256
#define MAX_EMITTED 100000

static long emitted;

static int load(yaml_parser_t *parser, yaml_document_t *document,
                const uint8_t *data, size_t size) {
    if (!data || size > MAX_INPUT || !yaml_parser_initialize(parser)) return 0;
    yaml_parser_set_input_string(parser, data, size);
    if (!yaml_parser_load(parser, document)) { yaml_parser_delete(parser); return 0; }
    return 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    yaml_parser_t parser;
    yaml_document_t document;
    if (load(&parser, &document, data, size)) {
        yaml_document_delete(&document);
        yaml_parser_delete(&parser);
    }
    return 0;
}

#ifndef PARSARIUM_FUZZER
static int emit(FILE *out, yaml_document_t *document, yaml_node_t *node, int depth) {
    if (!node || depth > MAX_DEPTH || ++emitted > MAX_EMITTED) return -1;
    switch (node->type) {
    case YAML_SCALAR_NODE:
        return typed_scalar(out, (const char *)node->data.scalar.value, node->data.scalar.length,
                            node->data.scalar.style == YAML_PLAIN_SCALAR_STYLE);
    case YAML_SEQUENCE_NODE:
        fputs("[\"seq\",[", out);
        for (yaml_node_item_t *item = node->data.sequence.items.start;
             item < node->data.sequence.items.top; item++) {
            if (item != node->data.sequence.items.start) fputc(',', out);
            if (emit(out, document, yaml_document_get_node(document, *item), depth + 1)) return -1;
        }
        fputs("]]", out);
        return 0;
    case YAML_MAPPING_NODE:
        fputs("[\"map\",[", out);
        for (yaml_node_pair_t *pair = node->data.mapping.pairs.start;
             pair < node->data.mapping.pairs.top; pair++) {
            yaml_node_t *key = yaml_document_get_node(document, pair->key);
            if (!key || key->type != YAML_SCALAR_NODE) return -1;
            if (pair != node->data.mapping.pairs.start) fputc(',', out);
            fputc('[', out);
            typed_string(out, (const char *)key->data.scalar.value, key->data.scalar.length);
            fputc(',', out);
            if (emit(out, document, yaml_document_get_node(document, pair->value), depth + 1)) return -1;
            fputc(']', out);
        }
        fputs("]]", out);
        return 0;
    default:
        return -1;
    }
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t *data = malloc(MAX_INPUT + 1);
    if (!data) { fclose(file); return 4; }
    size_t size = fread(data, 1, MAX_INPUT + 1, file);
    fclose(file);
    if (size > MAX_INPUT) { free(data); return 4; }
    yaml_parser_t parser;
    yaml_document_t document;
    if (!load(&parser, &document, data, size)) { free(data); return 5; }
    yaml_node_t *root = yaml_document_get_root_node(&document);
    int status = emit(stdout, &document, root, 1) ? 6 : 0;
    fputc('\n', stdout);
    yaml_document_delete(&document);
    /* Exactly one document: the next load must return the empty end-of-stream document. */
    yaml_document_t next;
    if (!status && (!yaml_parser_load(&parser, &next) || yaml_document_get_root_node(&next))) status = 7;
    else if (!status) yaml_document_delete(&next);
    yaml_parser_delete(&parser);
    free(data);
    return status;
}
#endif
