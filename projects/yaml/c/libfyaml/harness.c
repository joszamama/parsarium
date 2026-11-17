/* libfyaml document API over local bytes: fy_document_build_from_string with alias resolution.
 * The replay prints the built document as a typed tree; see typed.h for the adapter-side typing. */
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include <libfyaml.h>
#include "typed.h"

#define HARNESS_MAX_INPUT (1u << 20)
#define MAX_DEPTH 256
#define MAX_EMITTED 100000

static long emitted;

static struct fy_document *load(const uint8_t *data, size_t size) {
    static const struct fy_parse_cfg cfg = {
        .flags = FYPCF_QUIET | FYPCF_RESOLVE_DOCUMENT | FYPCF_DEFAULT_VERSION_1_2 | FYPCF_JSON_NONE,
    };
    if (!data || size > HARNESS_MAX_INPUT) return NULL;
    return fy_document_build_from_string(&cfg, (const char *)data, size);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct fy_document *document = load(data, size);
    if (document) fy_document_destroy(document);
    return 0;
}

#ifndef PARSARIUM_FUZZER
static int emit(FILE *out, struct fy_node *node, int depth) {
    if (!node || depth > MAX_DEPTH || ++emitted > MAX_EMITTED) return -1;
    void *iterator = NULL;
    switch (fy_node_get_type(node)) {
    case FYNT_SCALAR: {
        size_t length = 0;
        const char *text = fy_node_get_scalar(node, &length);
        enum fy_node_style style = fy_node_get_style(node);
        if (!text || style == FYNS_ALIAS) return -1;
        return typed_scalar(out, text, length, style == FYNS_PLAIN);
    }
    case FYNT_SEQUENCE: {
        struct fy_node *item;
        int first = 1;
        fputs("[\"seq\",[", out);
        while ((item = fy_node_sequence_iterate(node, &iterator))) {
            if (!first) fputc(',', out);
            first = 0;
            if (emit(out, item, depth + 1)) return -1;
        }
        fputs("]]", out);
        return 0;
    }
    case FYNT_MAPPING: {
        struct fy_node_pair *pair;
        int first = 1;
        fputs("[\"map\",[", out);
        while ((pair = fy_node_mapping_iterate(node, &iterator))) {
            struct fy_node *key = fy_node_pair_key(pair);
            size_t length = 0;
            const char *text = key && fy_node_get_type(key) == FYNT_SCALAR ? fy_node_get_scalar(key, &length) : NULL;
            if (!text) return -1;
            if (!first) fputc(',', out);
            first = 0;
            fputc('[', out);
            typed_string(out, text, length);
            fputc(',', out);
            if (emit(out, fy_node_pair_value(pair), depth + 1)) return -1;
            fputc(']', out);
        }
        fputs("]]", out);
        return 0;
    }
    default:
        return -1;
    }
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t *data = malloc(HARNESS_MAX_INPUT + 1);
    if (!data) { fclose(file); return 4; }
    size_t size = fread(data, 1, HARNESS_MAX_INPUT + 1, file);
    fclose(file);
    if (size > HARNESS_MAX_INPUT) { free(data); return 4; }
    struct fy_document *document = load(data, size);
    if (!document) { free(data); return 5; }
    int status = emit(stdout, fy_document_root(document), 1) ? 6 : 0;
    fputc('\n', stdout);
    fy_document_destroy(document);
    free(data);
    return status;
}
#endif
