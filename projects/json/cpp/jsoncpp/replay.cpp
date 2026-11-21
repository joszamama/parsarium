#include "harness.h"

#include <stdio.h>

#include <cmath>

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
    parsarium_json_result result;
    if (!parsarium_parse_json(input, size, &result)) return 5;
    printf("{\"arrays\":%lld,\"booleans\":%lld,\"max_depth\":%lld,\"nulls\":%lld,\"numbers\":[",
           (long long)result.arrays, (long long)result.booleans,
           (long long)result.max_depth, (long long)result.nulls);
    for (size_t i = 0; i < result.numbers.size(); i++) {
        const double number = result.numbers[i];
        // An out-of-range exponent parses to infinity; Infinity/-Infinity/NaN
        // tokens keep it a number the observer's JSON reader accepts.
        if (std::isnan(number)) printf("%sNaN", i ? "," : "");
        else if (std::isinf(number)) printf("%s%s", i ? "," : "", number > 0 ? "Infinity" : "-Infinity");
        else printf("%s%.17g", i ? "," : "", number);
    }
    printf("],\"objects\":%lld,\"root\":", (long long)result.objects);
    json_string(result.root);
    fputs(",\"strings\":", stdout);
    string_list(result.strings);
    fputs(",\"top_level_keys\":", stdout);
    string_list(result.top_level_keys);
    puts("}");
    return 0;
}
