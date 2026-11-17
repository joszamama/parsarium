/* Parser-only probe: gda_sql_parser_parse_string over every statement in the local bytes; no printing. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <libgda/libgda.h>
#include <sql-parser/gda-sql-parser.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 2;
    static char data[(1u << 20) + 1];
    size_t size = fread(data, 1, 1u << 20, file);
    fclose(file);
    if (size == 0 || size == (1u << 20) || memchr(data, 0, size)) return 2;
    data[size] = '\0';
    gda_init();
    GdaSqlParser *parser = gda_sql_parser_new();
    const gchar *cursor = data;
    int status = 0;
    while (cursor && *cursor) {
        while (*cursor == ' ' || *cursor == '\n' || *cursor == '\t' || *cursor == '\r') cursor++;
        if (!*cursor) break;
        const gchar *remain = NULL;
        GdaStatement *statement = gda_sql_parser_parse_string(parser, cursor, &remain, NULL);
        if (!statement) { status = 1; break; }
        g_object_unref(statement);
        cursor = remain;
    }
    g_object_unref(parser);
    return status;
}
