/* libgda: gda_sql_parser_parse_string(local SQL text) returns a GdaStatement whose
 * "structure" property is the GdaSqlStatement parse tree. The replay prints that tree with
 * the documented gda_sql_statement_serialize (JSON); summarize.py reads the oracle fields. */
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <libgda/libgda.h>
#include <sql-parser/gda-sql-parser.h>

/* Copies local bytes into a NUL-terminated string; rejects embedded NULs and oversize input. */
static char *text_from(const uint8_t *data, size_t size) {
    if (!data || size == 0 || size > (1u << 20) || memchr(data, 0, size)) return NULL;
    char *text = malloc(size + 1);
    if (!text) return NULL;
    memcpy(text, data, size);
    text[size] = '\0';
    return text;
}

/* Parses every statement in text; each GdaSqlStatement is serialized when out is non-NULL. */
static int parse_all(GdaSqlParser *parser, const char *text, FILE *out) {
    const gchar *cursor = text;
    int count = 0;
    if (out) fputs("[", out);
    while (cursor && *cursor) {
        while (*cursor == ' ' || *cursor == '\n' || *cursor == '\t' || *cursor == '\r') cursor++;
        if (!*cursor) break;
        const gchar *remain = NULL;
        GError *error = NULL;
        GdaStatement *statement = gda_sql_parser_parse_string(parser, cursor, &remain, &error);
        if (!statement) {
            if (out) fprintf(stderr, "parse error: %s\n", error && error->message ? error->message : "?");
            g_clear_error(&error);
            return -1;
        }
        if (out) {
            GdaSqlStatement *tree = NULL;
            g_object_get(statement, "structure", &tree, NULL);
            gchar *json = gda_sql_statement_serialize(tree);
            fprintf(out, "%s%s", count ? "," : "", json);
            g_free(json);
            gda_sql_statement_free(tree);
        }
        g_object_unref(statement);
        count++;
        cursor = remain;
    }
    if (out) fputs("]\n", out);
    return count;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    static GdaSqlParser *parser;
    if (!parser) {
        gda_init();
        parser = gda_sql_parser_new();
    }
    char *text = text_from(data, size);
    if (!text) return 0;
    parse_all(parser, text, NULL);
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
    gda_init();
    GdaSqlParser *parser = gda_sql_parser_new();
    int count = parse_all(parser, text, stdout);
    g_object_unref(parser);
    free(text);
    return count < 0 ? 5 : 0;
}
#endif
