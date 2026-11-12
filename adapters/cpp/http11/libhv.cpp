#include <http_parser.h>
#include <stdio.h>
#include <string.h>
#include "control.h"

/* libhv 1.3.1 bundles a C adaptation of Node's http-parser 2.9.1. */
struct state { char target[256]; size_t target_length; int headers_complete; };

static int on_url(http_parser *parser, const char *bytes, size_t length) {
    struct state *state = (struct state *)parser->data;
    if (state->target_length + length >= sizeof(state->target)) return -1;
    memcpy(state->target + state->target_length, bytes, length);
    state->target_length += length;
    state->target[state->target_length] = 0;
    return 0;
}

static int on_headers_complete(http_parser *parser) {
    ((struct state *)parser->data)->headers_complete = 1;
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: libhv control.http\n"); return 1; }
    char buffer[4096];
    size_t length = read_control(argv[1], buffer, sizeof(buffer));
    struct state state{};
    http_parser parser;
    http_parser_settings settings;
    http_parser_init(&parser, HTTP_REQUEST);
    parser.data = &state;
    http_parser_settings_init(&settings);
    settings.on_url = on_url;
    settings.on_headers_complete = on_headers_complete;
    size_t consumed = http_parser_execute(&parser, &settings, buffer, length);
    if (consumed != length || HTTP_PARSER_ERRNO(&parser) != HPE_OK || !state.headers_complete) {
        fprintf(stderr, "libhv HTTP parse failed\n");
        return 1;
    }
    printf("{\"method\":\"%s\",\"path\":\"%s\",\"version\":\"%u.%u\"}\n",
           http_method_str((enum http_method)parser.method), state.target,
           parser.http_major, parser.http_minor);
    return 0;
}
