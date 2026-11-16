#include "harness.h"
#include <stdio.h>
#include <string.h>

static void json_string(const char *value) {
    putchar('"');
    for (const unsigned char *at = (const unsigned char *)value; *at; ++at) {
        unsigned char c = *at;
        if (c == '"' || c == '\\') { putchar('\\'); putchar(c); }
        else if (c == '\n') fputs("\\n", stdout);
        else if (c == '\r') fputs("\\r", stdout);
        else if (c == '\t') fputs("\\t", stdout);
        else if (c >= 0x20 && c <= 0x7e) putchar(c);
        else printf("\\u%04x", c);
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
    fputs("{\"method\":", stdout); json_string(result.method);
    fputs(",\"path\":", stdout); json_string(result.path);
    fputs(",\"query\":", stdout); json_string(result.query);
    fputs(",\"version\":", stdout); json_string(result.version);
    fputs(",\"host\":", stdout); json_string(result.host);
    puts("}");
    return 0;
}
