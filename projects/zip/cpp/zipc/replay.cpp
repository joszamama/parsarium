#include "harness.h"

#include <stdio.h>
#include <stdlib.h>

static void json_string(const unsigned char *data, size_t size) {
    putchar('"');
    for (size_t i = 0; i < size; i++) {
        unsigned char c = data[i];
        if (c == '"' || c == '\\') {
            putchar('\\');
            putchar(c);
        } else if (c == '\n') {
            fputs("\\n", stdout);
        } else if (c == '\r') {
            fputs("\\r", stdout);
        } else if (c == '\t') {
            fputs("\\t", stdout);
        } else if (c >= 0x20 && c <= 0x7e) {
            putchar(c);
        } else {
            printf("\\u%04x", c);
        }
    }
    putchar('"');
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t input[1u << 20];
    size_t size = fread(input, 1, sizeof(input), file);
    if (ferror(file) || (size == sizeof(input) && fgetc(file) != EOF)) {
        fclose(file);
        return 4;
    }
    fclose(file);
    struct parsarium_zip_result result;
    if (!parsarium_parse_zip(input, size, &result)) return 5;
    fputs("{\"content\":", stdout);
    json_string(result.content, result.content_len);
    puts("}");
    return 0;
}
