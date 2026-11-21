#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "json.h"
#include "emit.h"

/* fjson_tokener_parse_ex on the exact local byte length in strict mode. The
 * header documents detecting trailing bytes through tok->char_offset; only JSON
 * whitespace may follow the value. A JSON null root is a NULL object with
 * fjson_tokener_success, so success is reported separately from the object. */
static int parse_json(const uint8_t *data, size_t size, struct fjson_object **out) {
    *out = NULL;
    if (!data || size == 0 || size > (1u << 20)) return 0;
    struct fjson_tokener *tok = fjson_tokener_new();
    if (!tok) return 0;
    fjson_tokener_set_flags(tok, FJSON_TOKENER_STRICT);
    struct fjson_object *root = fjson_tokener_parse_ex(tok, (const char *)data, (int)size);
    int ok = fjson_tokener_get_error(tok) == fjson_tokener_success;
    if (ok) {
        for (size_t end = (size_t)tok->char_offset; end < size; end++) {
            char c = (char)data[end];
            if (c != ' ' && c != '\t' && c != '\n' && c != '\r') {
                ok = 0;
                break;
            }
        }
    }
    if (!ok && root) {
        fjson_object_put(root);
        root = NULL;
    }
    fjson_tokener_free(tok);
    *out = root;
    return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct fjson_object *root;
    if (parse_json(data, size, &root) && root) fjson_object_put(root);
    return 0;
}

#ifndef PARSARIUM_FUZZER
/* Prints the fjson_object tree: members in iterator order, fjson_type_int as
 * integers and fjson_type_double as floats. */
static void emit(FILE *out, struct fjson_object *value) {
    switch (fjson_object_get_type(value)) {
    case fjson_type_object: {
        struct fjson_object_iterator it = fjson_object_iter_begin(value);
        struct fjson_object_iterator end = fjson_object_iter_end(value);
        int first = 1;
        fputc('{', out);
        while (!fjson_object_iter_equal(&it, &end)) {
            const char *name = fjson_object_iter_peek_name(&it);
            if (!first) fputc(',', out);
            first = 0;
            emit_string(out, name, strlen(name));
            fputc(':', out);
            emit(out, fjson_object_iter_peek_value(&it));
            fjson_object_iter_next(&it);
        }
        fputc('}', out);
        break;
    }
    case fjson_type_array:
        fputc('[', out);
        for (int i = 0; i < fjson_object_array_length(value); i++) {
            if (i) fputc(',', out);
            emit(out, fjson_object_array_get_idx(value, i));
        }
        fputc(']', out);
        break;
    case fjson_type_int: emit_int(out, fjson_object_get_int64(value)); break;
    case fjson_type_double: emit_double(out, fjson_object_get_double(value)); break;
    case fjson_type_string:
        emit_string(out, fjson_object_get_string(value), (size_t)fjson_object_get_string_len(value));
        break;
    case fjson_type_boolean: fputs(fjson_object_get_boolean(value) ? "true" : "false", out); break;
    case fjson_type_null: fputs("null", out); break;
    default: fputs("\"<unexpected libfastjson type>\"", out); break;
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
    struct fjson_object *root;
    int ok = parse_json(data, size, &root);
    free(data);
    if (!ok) return 5;
    emit(stdout, root);
    fputc('\n', stdout);
    if (root) fjson_object_put(root);
    return 0;
}
#endif
