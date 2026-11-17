/* Parser-only probe: yajl_parse + yajl_complete_parse on the local bytes with
 * no-op callbacks (so yajl still converts integer and double tokens); no printing. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include <yajl/yajl_parse.h>

static int on_null(void *c) { (void)c; return 1; }
static int on_bool(void *c, int v) { (void)c; (void)v; return 1; }
static int on_int(void *c, long long v) { (void)c; (void)v; return 1; }
static int on_double(void *c, double v) { (void)c; (void)v; return 1; }
static int on_string(void *c, const unsigned char *s, size_t n) { (void)c; (void)s; (void)n; return 1; }
static int on_mark(void *c) { (void)c; return 1; }

static const yajl_callbacks callbacks = {
    on_null, on_bool, on_int, on_double, NULL, on_string,
    on_mark, on_string, on_mark, on_mark, on_mark
};

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 2;
    static unsigned char data[1u << 20];
    size_t size = fread(data, 1, sizeof data, file);
    fclose(file);
    if (size == 0 || size == sizeof data) return 2;
    yajl_handle handle = yajl_alloc(&callbacks, NULL, NULL);
    if (!handle) return 1;
    int ok = yajl_parse(handle, data, size) == yajl_status_ok
          && yajl_complete_parse(handle) == yajl_status_ok;
    yajl_free(handle);
    return ok ? 0 : 1;
}
