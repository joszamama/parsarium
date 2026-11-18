#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "json.h"
#include "emit.h"

static struct json_value_s *parse_json(const uint8_t *data, size_t size) {
    if (!data || size > (1u << 20)) return NULL;
    return json_parse(data, size);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct json_value_s *root = parse_json(data, size);
    free(root);
    return 0;
}

#ifndef PARSARIUM_FUZZER
/* Prints the parsed json.h DOM: object elements in linked-list order, decoded
 * strings, and each json_number_s as the number text json.h stored, so the
 * oracle reads integer versus float kind from the literal json.h kept. */
static void emit(FILE *out, const struct json_value_s *value) {
    switch (value->type) {
    case json_type_object: {
        const struct json_object_s *object = json_value_as_object((struct json_value_s *)value);
        fputc('{', out);
        for (const struct json_object_element_s *e = object->start; e; e = e->next) {
            if (e != object->start) fputc(',', out);
            emit_string(out, e->name->string, e->name->string_size);
            fputc(':', out);
            emit(out, e->value);
        }
        fputc('}', out);
        break;
    }
    case json_type_array: {
        const struct json_array_s *array = json_value_as_array((struct json_value_s *)value);
        fputc('[', out);
        for (const struct json_array_element_s *e = array->start; e; e = e->next) {
            if (e != array->start) fputc(',', out);
            emit(out, e->value);
        }
        fputc(']', out);
        break;
    }
    case json_type_number: {
        const struct json_number_s *number = json_value_as_number((struct json_value_s *)value);
        fwrite(number->number, 1, number->number_size, out);
        break;
    }
    case json_type_string: {
        const struct json_string_s *string = json_value_as_string((struct json_value_s *)value);
        emit_string(out, string->string, string->string_size);
        break;
    }
    case json_type_true: fputs("true", out); break;
    case json_type_false: fputs("false", out); break;
    case json_type_null: fputs("null", out); break;
    default: fputs("\"<unexpected json.h type>\"", out); break;
    }
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 3;
    uint8_t *data = malloc((1u << 20) + 1);
    if (!data) { fclose(file); return 4; }
    size_t size = fread(data, 1, 1u << 20, file);
    if (ferror(file) || (size == (1u << 20) && fgetc(file) != EOF)) {
        free(data); fclose(file); return 4;
    }
    fclose(file);
    struct json_value_s *root = parse_json(data, size);
    free(data);
    if (!root) return 5;
    emit(stdout, root);
    fputc('\n', stdout);
    free(root);
    return 0;
}
#endif
