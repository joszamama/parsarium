/* toml-c harness: toml_parse(toml, errbuf, size) on the local bytes, then walk the
 * returned toml_table_t tree with the documented toml.h accessors and print the typed tree. */
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "toml.h"
#include "emit.h"

#define MAX_INPUT (1u << 20)

static toml_table_t *parse_toml(const uint8_t *data, size_t size, char *errbuf, int errsize) {
    if (!data || size > MAX_INPUT || memchr(data, 0, size)) return NULL;
    char *text = malloc(size + 1);
    if (!text) return NULL;
    memcpy(text, data, size);
    text[size] = 0;
    toml_table_t *root = toml_parse(text, errbuf, errsize);
    free(text);
    return root;
}

/* toml_timestamp_t.kind: 'd'atetime with offset (tz minutes), 'l'ocal datetime,
 * 'D'ate-local, 't'ime-local. */
static int emit_timestamp(const toml_timestamp_t *ts) {
    long usec = (long)ts->millisec * 1000;
    switch (ts->kind) {
    case 'd':
        emit_offset_datetime(ts->year, ts->month, ts->day, ts->hour, ts->minute, ts->second,
                             usec, ts->tz);
        return 0;
    case 'l':
        emit_local_datetime(ts->year, ts->month, ts->day, ts->hour, ts->minute, ts->second, usec);
        return 0;
    case 'D':
        emit_local_date(ts->year, ts->month, ts->day);
        return 0;
    case 't':
        emit_local_time(ts->hour, ts->minute, ts->second, usec);
        return 0;
    default:
        return -1;
    }
}

static int emit_table(const toml_table_t *table);
static int emit_array(const toml_array_t *array);

/* Typed accessors in an order where each rejects the others' raw forms
 * (integers before doubles, since the double conversion also accepts integer text). */
static int emit_value_in(const toml_table_t *table, const char *key) {
    toml_value_t v = toml_table_string(table, key);
    if (v.ok) { emit_scalar("string", v.u.s, (size_t)v.u.sl); free(v.u.s); return 0; }
    v = toml_table_bool(table, key);
    if (v.ok) { emit_scalar_text("bool", v.u.b ? "true" : "false"); return 0; }
    v = toml_table_int(table, key);
    if (v.ok) { emit_integer(v.u.i); return 0; }
    v = toml_table_double(table, key);
    if (v.ok) return emit_float(v.u.d);
    v = toml_table_timestamp(table, key);
    if (v.ok) return emit_timestamp(&v.u.ts);
    return -1;
}

static int emit_value_at(const toml_array_t *array, int index) {
    toml_value_t v = toml_array_string(array, index);
    if (v.ok) { emit_scalar("string", v.u.s, (size_t)v.u.sl); free(v.u.s); return 0; }
    v = toml_array_bool(array, index);
    if (v.ok) { emit_scalar_text("bool", v.u.b ? "true" : "false"); return 0; }
    v = toml_array_int(array, index);
    if (v.ok) { emit_integer(v.u.i); return 0; }
    v = toml_array_double(array, index);
    if (v.ok) return emit_float(v.u.d);
    v = toml_array_timestamp(array, index);
    if (v.ok) return emit_timestamp(&v.u.ts);
    return -1;
}

static int emit_table(const toml_table_t *table) {
    putchar('{');
    int count = toml_table_len(table);
    for (int i = 0; i < count; i++) {
        int keylen = 0;
        const char *key = toml_table_key(table, i, &keylen);
        if (!key) return -1;
        if (i) putchar(',');
        emit_json_string(key, (size_t)keylen);
        putchar(':');
        toml_array_t *array = toml_table_array(table, key);
        toml_table_t *child = toml_table_table(table, key);
        int rc = array ? emit_array(array) : child ? emit_table(child) : emit_value_in(table, key);
        if (rc) return rc;
    }
    putchar('}');
    return 0;
}

static int emit_array(const toml_array_t *array) {
    putchar('[');
    int count = toml_array_len(array);
    for (int i = 0; i < count; i++) {
        if (i) putchar(',');
        toml_table_t *table = toml_array_table(array, i);
        toml_array_t *child = toml_array_array(array, i);
        int rc = table ? emit_table(table) : child ? emit_array(child) : emit_value_at(array, i);
        if (rc) return rc;
    }
    putchar(']');
    return 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    char errbuf[200];
    toml_table_t *root = parse_toml(data, size, errbuf, sizeof errbuf);
    if (root) toml_free(root);
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
    char errbuf[200] = {0};
    toml_table_t *root = parse_toml(data, size, errbuf, sizeof errbuf);
    free(data);
    if (!root) { fprintf(stderr, "toml_parse failed: %s\n", errbuf); return 5; }
    int rc = emit_table(root);
    putchar('\n');
    toml_free(root);
    if (rc) { fprintf(stderr, "value not representable in the typed tree\n"); return 6; }
    return 0;
}
#endif
