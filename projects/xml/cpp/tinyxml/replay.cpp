#include "harness.h"

#include <stdio.h>

static void json_string(const std::string &text) {
    putchar('"');
    for (unsigned char c : text) {
        if (c == '"' || c == '\\') {
            putchar('\\');
            putchar(c);
        } else if (c < 0x20) {
            printf("\\u%04x", c);
        } else {
            putchar(c);  // UTF-8 bytes pass through unchanged
        }
    }
    putchar('"');
}

static void string_list(const std::vector<std::string> &items) {
    putchar('[');
    for (size_t i = 0; i < items.size(); i++) {
        if (i) putchar(',');
        json_string(items[i]);
    }
    putchar(']');
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    static uint8_t input[1u << 20];
    size_t size = fread(input, 1, sizeof(input), file);
    if (ferror(file) || (size == sizeof(input) && fgetc(file) != EOF)) {
        fclose(file);
        return 4;
    }
    fclose(file);
    parsarium_xml_result result;
    std::string error;
    if (!parsarium_parse_xml(input, size, &result, &error)) {
        if (!error.empty()) fprintf(stderr, "%s\n", error.c_str());
        return 5;
    }
    fputs("{\"attributes\":", stdout);
    string_list(result.attributes);
    fputs(",\"elements\":", stdout);
    string_list(result.elements);
    printf(",\"max_depth\":%lld,\"namespace_declarations\":%lld,\"namespaces\":",
           (long long)result.max_depth, (long long)result.namespace_declarations);
    string_list(result.namespaces);
    fputs(",\"root\":", stdout);
    json_string(result.root);
    fputs(",\"text\":", stdout);
    string_list(result.text);
    puts("}");
    return 0;
}
