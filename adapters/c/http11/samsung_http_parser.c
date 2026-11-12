/* Samsung v2.5.0 is a tagged fork of the Node/Joyent HTTP parser family. */
#include <http_parser.h>
#include <stdio.h>
#include <string.h>
#include "control.h"

struct state { char path[256]; size_t path_length; int headers_complete; };

static int on_url(http_parser *parser, const char *bytes, size_t length) {
    struct state *state = parser->data;
    if (state->path_length + length >= sizeof(state->path)) return -1;
    memcpy(state->path + state->path_length, bytes, length);
    state->path_length += length;
    state->path[state->path_length] = 0;
    return 0;
}

static int on_headers_complete(http_parser *parser) {
    ((struct state *)parser->data)->headers_complete = 1;
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: samsung-http-parser control.http\n"); return 1; }
    char buffer[4096];
    size_t length = read_control(argv[1], buffer, sizeof(buffer));
    struct state state = {0};
    http_parser parser;
    http_parser_settings settings;
    http_parser_init(&parser, HTTP_REQUEST);
    parser.data = &state;
    http_parser_settings_init(&settings);
    settings.on_url = on_url;
    settings.on_headers_complete = on_headers_complete;
    size_t consumed = http_parser_execute(&parser, &settings, buffer, length);
    if (consumed != length || HTTP_PARSER_ERRNO(&parser) != HPE_OK || !state.headers_complete) {
        fprintf(stderr, "samsung-http-parser parse failed\n");
        return 1;
    }
    printf("{\"method\":\"%s\",\"path\":\"%s\",\"version\":\"%u.%u\"}\n",
           http_method_str((enum http_method)parser.method), state.path,
           parser.http_major, parser.http_minor);
    return 0;
}
