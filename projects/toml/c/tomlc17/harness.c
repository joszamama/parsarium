/* tomlc17 harness: toml_parse(src, len) on the local bytes, then walk the returned
 * toml_datum_t tree (documented type/u.tab/u.arr/u.ts fields) and print the typed tree. */
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "tomlc17.h"
#include "emit.h"

#define MAX_INPUT (1u << 20)

static int emit_datum(toml_datum_t datum) {
    switch (datum.type) {
    case TOML_TABLE:
        putchar('{');
        for (int32_t i = 0; i < datum.u.tab.size; i++) {
            if (i) putchar(',');
            emit_json_string(datum.u.tab.key[i], (size_t)datum.u.tab.len[i]);
            putchar(':');
            if (emit_datum(datum.u.tab.value[i])) return -1;
        }
        putchar('}');
        return 0;
    case TOML_ARRAY:
        putchar('[');
        for (int32_t i = 0; i < datum.u.arr.size; i++) {
            if (i) putchar(',');
            if (emit_datum(datum.u.arr.elem[i])) return -1;
        }
        putchar(']');
        return 0;
    case TOML_STRING:
        emit_scalar("string", datum.u.str.ptr, (size_t)datum.u.str.len);
        return 0;
    case TOML_INT64:
        emit_integer(datum.u.int64);
        return 0;
    case TOML_FP64:
        return emit_float(datum.u.fp64);
    case TOML_BOOLEAN:
        emit_scalar_text("bool", datum.u.boolean ? "true" : "false");
        return 0;
    case TOML_DATETIMETZ:
        emit_offset_datetime(datum.u.ts.year, datum.u.ts.month, datum.u.ts.day,
                             datum.u.ts.hour, datum.u.ts.minute, datum.u.ts.second,
                             datum.u.ts.usec, datum.u.ts.tz);
        return 0;
    case TOML_DATETIME:
        emit_local_datetime(datum.u.ts.year, datum.u.ts.month, datum.u.ts.day,
                            datum.u.ts.hour, datum.u.ts.minute, datum.u.ts.second,
                            datum.u.ts.usec);
        return 0;
    case TOML_DATE:
        emit_local_date(datum.u.ts.year, datum.u.ts.month, datum.u.ts.day);
        return 0;
    case TOML_TIME:
        emit_local_time(datum.u.ts.hour, datum.u.ts.minute, datum.u.ts.second,
                        datum.u.ts.usec);
        return 0;
    default:
        return -1;
    }
}

static toml_result_t parse_toml(const uint8_t *data, size_t size) {
    return toml_parse((const char *)data, (int)size);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (!data || size > MAX_INPUT) return 0;
    toml_result_t result = parse_toml(data, size);
    toml_free(result);
    return 0;
}

#ifndef PARSARIUM_FUZZER
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t *data = malloc(MAX_INPUT + 1);
    if (!data) { fclose(file); return 4; }
    size_t size = fread(data, 1, MAX_INPUT + 1, file);
    fclose(file);
    if (size > MAX_INPUT) { free(data); return 4; }
    toml_result_t result = parse_toml(data, size);
    free(data);
    if (!result.ok) {
        fprintf(stderr, "toml_parse failed: %s\n", result.errmsg);
        toml_free(result);
        return 5;
    }
    int rc = emit_datum(result.toptab);
    putchar('\n');
    toml_free(result);
    if (rc) { fprintf(stderr, "value not representable in the typed tree\n"); return 6; }
    return 0;
}
#endif
