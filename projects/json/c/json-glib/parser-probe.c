/* Parser-only probe: strict json_parser_load_from_data on the local bytes, then free; no printing. */
#include <stdio.h>

#include <json-glib/json-glib.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = fopen(argv[1], "rb");
    if (!file) return 2;
    static char data[1u << 20];
    size_t size = fread(data, 1, sizeof data, file);
    fclose(file);
    if (size == 0 || size == sizeof data) return 2;
    JsonParser *parser = json_parser_new();
    json_parser_set_strict(parser, TRUE);
    GError *error = NULL;
    int status = json_parser_load_from_data(parser, data, (gssize)size, &error) ? 0 : 1;
    g_clear_error(&error);
    g_object_unref(parser);
    return status;
}
