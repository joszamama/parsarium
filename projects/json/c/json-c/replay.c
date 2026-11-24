#include "harness.h"

#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2 && !(argc == 3 && strcmp(argv[2], "--tree") == 0)) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    static uint8_t input[1u << 20];
    size_t size = fread(input, 1, sizeof(input), file);
    if (ferror(file) || (size == sizeof(input) && fgetc(file) != EOF)) {
        fclose(file);
        return 4;
    }
    fclose(file);
    struct json_object *root;
    if (!parsarium_parse_json(input, size, &root)) {
        const char *error = parsarium_json_error();
        if (*error) fprintf(stderr, "%s\n", error);
        return 5;
    }
    if (argc == 3) {
        parsarium_print_tree(root);
        putchar('\n');
    } else {
        parsarium_print_summary(root);
    }
    json_object_put(root);
    return 0;
}
