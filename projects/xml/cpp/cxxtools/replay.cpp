#include "harness.h"

#include <stdio.h>

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
    std::string json;
    if (!parsarium_parse_xml(input, size, &json)) return 5;
    printf("%s\n", json.c_str());
    return 0;
}
