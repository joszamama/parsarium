#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include <json-glib/json-glib.h>
#include "emit.h"

/* Strict RFC 8259 mode, then json_parser_load_from_data with the exact byte length. */
static JsonParser *parse_json(const uint8_t *data, size_t size) {
    if (!data || size == 0 || size > (1u << 20)) return NULL;
    JsonParser *parser = json_parser_new();
    json_parser_set_strict(parser, TRUE);
    GError *error = NULL;
    if (!json_parser_load_from_data(parser, (const gchar *)data, (gssize)size, &error)
            || json_parser_get_root(parser) == NULL) {
        g_clear_error(&error);
        g_object_unref(parser);
        return NULL;
    }
    return parser;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    JsonParser *parser = parse_json(data, size);
    if (parser) g_object_unref(parser);
    return 0;
}

#ifndef PARSARIUM_FUZZER
/* Prints the JsonNode tree: members in json_object_get_members order (insertion
 * order), G_TYPE_INT64 values as integers and G_TYPE_DOUBLE values as floats. */
static void emit(FILE *out, JsonNode *node) {
    switch (json_node_get_node_type(node)) {
    case JSON_NODE_OBJECT: {
        JsonObject *object = json_node_get_object(node);
        GList *members = json_object_get_members(object);
        fputc('{', out);
        for (GList *item = members; item; item = item->next) {
            const char *name = item->data;
            if (item != members) fputc(',', out);
            emit_string(out, name, strlen(name));
            fputc(':', out);
            emit(out, json_object_get_member(object, name));
        }
        g_list_free(members);
        fputc('}', out);
        break;
    }
    case JSON_NODE_ARRAY: {
        JsonArray *array = json_node_get_array(node);
        fputc('[', out);
        for (guint i = 0; i < json_array_get_length(array); i++) {
            if (i) fputc(',', out);
            emit(out, json_array_get_element(array, i));
        }
        fputc(']', out);
        break;
    }
    case JSON_NODE_NULL: fputs("null", out); break;
    case JSON_NODE_VALUE: {
        GType type = json_node_get_value_type(node);
        if (type == G_TYPE_INT64) emit_int(out, json_node_get_int(node));
        else if (type == G_TYPE_DOUBLE) emit_double(out, json_node_get_double(node));
        else if (type == G_TYPE_BOOLEAN) fputs(json_node_get_boolean(node) ? "true" : "false", out);
        else if (type == G_TYPE_STRING) {
            const char *text = json_node_get_string(node);
            emit_string(out, text, strlen(text));
        } else fputs("\"<unexpected JSON-GLib value type>\"", out);
        break;
    }
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
    JsonParser *parser = parse_json(data, size);
    free(data);
    if (!parser) return 5;
    emit(stdout, json_parser_get_root(parser));
    fputc('\n', stdout);
    g_object_unref(parser);
    return 0;
}
#endif
