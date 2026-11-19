#include "harness.h"
#include <stdio.h>

static void print_json_string(const char *text, size_t length) {
    putchar('"');
    for (size_t i = 0; i < length; i++) {
        const unsigned char *c = (const unsigned char *)text + i;
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
    static uint8_t data[1u << 20];
    size_t size = fread(data, 1, sizeof(data), file);
    if (ferror(file) || (size == sizeof(data) && fgetc(file) != EOF)) {
        fclose(file); return 4;
    }
    fclose(file);
    struct parsarium_http_result result;
    if (!parsarium_parse_http(data, size, &result)) return 5;
    printf("{\"method\":"); print_json_string(result.method, result.method_len);
    printf(",\"path\":"); print_json_string(result.path, result.path_len);
    printf(",\"version\":\"1.%d\"}\n", result.minor);
    return 0;
}
