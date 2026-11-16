#include "harness.h"

#include <stdio.h>
#include <stdlib.h>

static void json_string(const char *value) {
    putchar('"');
    for (const unsigned char *c = (const unsigned char *)value; *c; c++) {
        if (*c == '"' || *c == '\\') printf("\\%c", *c);
        else if (*c < 0x20 || *c >= 0x7f) printf("\\u%04x", *c);
        else putchar(*c);
    }
    putchar('"');
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    /* One byte past the cap distinguishes an over-cap file from an exact fit. */
    uint8_t *data = malloc(PARSARIUM_HTTP_MAX_INPUT + 1);
    if (!data) {
        fclose(file);
        return 4;
    }
    size_t size = fread(data, 1, PARSARIUM_HTTP_MAX_INPUT + 1, file);
    int read_error = ferror(file);
    fclose(file);
    if (read_error || size > PARSARIUM_HTTP_MAX_INPUT) {
        free(data);
        return 4;
    }
    struct parsarium_http_result result;
    int ok = parsarium_parse_http(data, size, &result);
    free(data);
    parsarium_http_teardown();
    if (!ok) return 5;
    printf("{\"method\":");
    json_string(result.method);
    printf(",\"path\":");
    json_string(result.path);
    printf(",\"host\":");
    json_string(result.host);
    printf("}\n");
    parsarium_http_result_clear(&result);
    return 0;
}
