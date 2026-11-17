#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "json.h"
#include "emit.h"

static json_value *parse_json(const uint8_t *data, size_t size) {
    if (!data || size > (1u << 20)) return NULL;
    json_settings settings = {0};
    char error[json_error_max];
    return json_parse_ex(&settings, (const json_char *)data, size, error);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    json_value *root = parse_json(data, size);
    if (root) json_value_free(root);
    return 0;
}

#ifndef PARSARIUM_FUZZER
/* Prints the parsed json_value tree: object members in stored order,
 * json_integer as integers and json_double as floats. */
static void emit(FILE *out, const json_value *value) {
    switch (value->type) {
    case json_object:
        fputc('{', out);
        for (unsigned int i = 0; i < value->u.object.length; i++) {
            if (i) fputc(',', out);
            emit_string(out, value->u.object.values[i].name, value->u.object.values[i].name_length);
            fputc(':', out);
            emit(out, value->u.object.values[i].value);
        }
        fputc('}', out);
        break;
    case json_array:
        fputc('[', out);
        for (unsigned int i = 0; i < value->u.array.length; i++) {
            if (i) fputc(',', out);
            emit(out, value->u.array.values[i]);
        }
        fputc(']', out);
        break;
    case json_integer: emit_int(out, value->u.integer); break;
    case json_double: emit_double(out, value->u.dbl); break;
    case json_string: emit_string(out, value->u.string.ptr, value->u.string.length); break;
    case json_boolean: fputs(value->u.boolean ? "true" : "false", out); break;
    case json_null: fputs("null", out); break;
    default: fputs("\"<unexpected json-parser type>\"", out); break;
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
    json_value *root = parse_json(data, size);
    free(data);
    if (!root) return 5;
    emit(stdout, root);
    fputc('\n', stdout);
    json_value_free(root);
    return 0;
}
#endif
