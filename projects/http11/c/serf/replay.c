#include "harness.h"
#include <stdio.h>

static void print_json_string(const char *text, size_t length) {
    putchar('"');
    for (size_t i = 0; i < length; i++) {
        const unsigned char *p = (const unsigned char *)text + i;
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
    static uint8_t data[1u << 20];
    size_t size = fread(data, 1, sizeof(data), file);
    if (ferror(file) || (size == sizeof(data) && fgetc(file) != EOF)) {
        fclose(file); return 4;
    }
    fclose(file);
    struct parsarium_http_response result;
    if (!parsarium_parse_http_response(data, size, &result)) return 5;
    printf("{\"version\":\"%d.%d\",\"status\":%d,\"reason\":", result.major, result.minor,
           result.status);
    print_json_string(result.reason, result.reason_len);
    printf(",\"content_type\":");
    if (result.has_content_type) print_json_string(result.content_type, result.content_type_len);
    else printf("null");
    printf(",\"body\":");
    print_json_string(result.body, result.body_len);
    printf("}\n");
    parsarium_http_response_free(&result);
    return 0;
}
