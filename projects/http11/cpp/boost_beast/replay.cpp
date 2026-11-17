#include "harness.h"
#include <stdio.h>
static void print_json_string(const std::string &value) {
    putchar('"');
    for (unsigned char c : value) {
        if (c == '"' || c == '\\') printf("\\%c", c);
        else if (c < 0x20 || c >= 0x7f) printf("\\u%04x", c);
        else putchar(c);
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
    printf("{\"method\":"); print_json_string(result.method);
    printf(",\"path\":"); print_json_string(result.path);
    printf(",\"version\":\"%d.%d\",\"host\":", result.major, result.minor);
    print_json_string(result.host);
    printf("}\n");
    return 0;
}
