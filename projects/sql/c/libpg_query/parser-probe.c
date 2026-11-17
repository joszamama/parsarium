/* Parser-only probe: pg_query_parse on the local bytes, then free; no printing. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "pg_query.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 2;
    static char data[(1u << 20) + 1];
    size_t size = fread(data, 1, 1u << 20, file);
    fclose(file);
    if (size == 0 || size == (1u << 20) || memchr(data, 0, size)) return 2;
    data[size] = '\0';
    PgQueryParseResult result = pg_query_parse(data);
    int status = result.error ? 1 : 0;
    pg_query_free_parse_result(result);
    return status;
}
