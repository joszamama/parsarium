/* libpg_query: pg_query_parse(local SQL text) returns the PostgreSQL raw parse tree,
 * serialized by libpg_query as JSON. The replay prints that tree unchanged; summarize.py
 * reads the oracle fields from it. */
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "pg_query.h"

/* Copies local bytes into a NUL-terminated string; rejects embedded NULs and oversize input. */
static char *text_from(const uint8_t *data, size_t size) {
    if (!data || size == 0 || size > (1u << 20) || memchr(data, 0, size)) return NULL;
    char *text = malloc(size + 1);
    if (!text) return NULL;
    memcpy(text, data, size);
    text[size] = '\0';
    return text;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    char *text = text_from(data, size);
    if (!text) return 0;
    PgQueryParseResult result = pg_query_parse(text);
    pg_query_free_parse_result(result);
    free(text);
    return 0;
}

#ifndef PARSARIUM_FUZZER
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t *data = malloc((1u << 20) + 1);
    if (!data) { fclose(file); return 4; }
    size_t size = fread(data, 1, (1u << 20) + 1, file);
    fclose(file);
    char *text = text_from(data, size);
    free(data);
    if (!text) return 4;
    PgQueryParseResult result = pg_query_parse(text);
    free(text);
    if (result.error) {
        fprintf(stderr, "parse error: %s\n", result.error->message);
        pg_query_free_parse_result(result);
        return 5;
    }
    fputs(result.parse_tree, stdout);
    fputc('\n', stdout);
    pg_query_free_parse_result(result);
    return 0;
}
#endif
