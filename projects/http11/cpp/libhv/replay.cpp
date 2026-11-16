#include "harness.h"
#include <stdio.h>

static void print_json_string(const char *text) {
    putchar('"');
    for (const unsigned char *p = (const unsigned char *)text; *p; ++p) {
        if (*p == '"' || *p == '\\') printf("\\%c", *p);
        else if (*p < 0x20 || *p >= 0x7f) printf("\\u%04x", *p);
        else putchar(*p);
    }
    putchar('"');
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t data[1u << 20];
    size_t size = fread(data, 1, sizeof(data), file);
    if (ferror(file) || (size == sizeof(data) && fgetc(file) != EOF)) {
        fclose(file); return 4;
    }
    fclose(file);
    struct parsarium_http_result result;
    if (!parsarium_parse_http(data, size, &result)) return 5;
    printf("{\"method\":"); print_json_string(result.method);
    printf(",\"path\":"); print_json_string(result.path);
    printf(",\"version\":\"%d.%d\"}\n", result.major, result.minor);
    return 0;
}
