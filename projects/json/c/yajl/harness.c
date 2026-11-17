#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include <yajl/yajl_parse.h>
#include "emit.h"

/* Event printer for the documented yajl_parse callback API. yajl's own lexer
 * classifies integer versus double tokens and calls yajl_integer/yajl_double;
 * map keys and values arrive in source order. The printer only places commas. */
typedef struct { FILE *out; int depth; int need_comma[256]; int after_key; } printer;

static void sep(printer *p) {
    if (p->after_key) { p->after_key = 0; return; }
    if (p->depth > 0) {
        if (p->need_comma[p->depth]) fputc(',', p->out);
        p->need_comma[p->depth] = 1;
    }
}
static int on_null(void *c) { printer *p = c; if (!p) return 1; sep(p); fputs("null", p->out); return 1; }
static int on_bool(void *c, int v) { printer *p = c; if (!p) return 1; sep(p); fputs(v ? "true" : "false", p->out); return 1; }
static int on_int(void *c, long long v) { printer *p = c; if (!p) return 1; sep(p); emit_int(p->out, (int64_t)v); return 1; }
static int on_double(void *c, double v) { printer *p = c; if (!p) return 1; sep(p); emit_double(p->out, v); return 1; }
static int on_string(void *c, const unsigned char *s, size_t n) {
    printer *p = c; if (!p) return 1; sep(p); emit_string(p->out, (const char *)s, n); return 1;
}
static int on_key(void *c, const unsigned char *s, size_t n) {
    printer *p = c; if (!p) return 1; sep(p); emit_string(p->out, (const char *)s, n);
    fputc(':', p->out); p->after_key = 1; return 1;
}
static int on_open(printer *p, int ch) {
    sep(p); fputc(ch, p->out);
    if (++p->depth >= 256) return 0;
    p->need_comma[p->depth] = 0; return 1;
}
static int on_start_map(void *c) { printer *p = c; return p ? on_open(p, '{') : 1; }
static int on_end_map(void *c) { printer *p = c; if (!p) return 1; p->depth--; fputc('}', p->out); return 1; }
static int on_start_array(void *c) { printer *p = c; return p ? on_open(p, '[') : 1; }
static int on_end_array(void *c) { printer *p = c; if (!p) return 1; p->depth--; fputc(']', p->out); return 1; }

static const yajl_callbacks callbacks = {
    on_null, on_bool, on_int, on_double, NULL, on_string,
    on_start_map, on_key, on_end_map, on_start_array, on_end_array
};

/* Documented yajl_parse(handle, bytes, length) then yajl_complete_parse with the
 * default configuration: no comments, no trailing garbage, one value. */
static int parse_json(const uint8_t *data, size_t size, printer *p) {
    if (!data || size > (1u << 20)) return 0;
    yajl_handle handle = yajl_alloc(&callbacks, NULL, p);
    if (!handle) return 0;
    int ok = yajl_parse(handle, data, size) == yajl_status_ok
          && yajl_complete_parse(handle) == yajl_status_ok;
    yajl_free(handle);
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parse_json(data, size, NULL);
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
    printer p = { stdout, 0, {0}, 0 };
    int ok = parse_json(data, size, &p);
    free(data);
    if (!ok || p.depth != 0) return 5;
    fputc('\n', stdout);
    return 0;
}
#endif
