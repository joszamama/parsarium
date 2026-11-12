#include <llhttp.h>
#include <stdio.h>
#include <string.h>
#include "control.h"

struct state { char path[256]; size_t path_length; int headers_complete; };

static int on_url(llhttp_t *parser, const char *bytes, size_t length) {
    struct state *state = parser->data;
    if (state->path_length + length >= sizeof(state->path)) return -1;
    memcpy(state->path + state->path_length, bytes, length);
    state->path_length += length;
    state->path[state->path_length] = 0;
    return 0;
}

static int on_headers_complete(llhttp_t *parser) {
    ((struct state *)parser->data)->headers_complete = 1;
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: HTTPParserC control.http\n"); return 1; }
    char buffer[4096];
    size_t length = read_control(argv[1], buffer, sizeof(buffer));
    struct state state = {0};
    llhttp_settings_t settings;
    llhttp_settings_init(&settings);
    settings.on_url = on_url;
    settings.on_headers_complete = on_headers_complete;
    llhttp_t parser;
    llhttp_init(&parser, LLHTTP_REQUEST, &settings);
    parser.data = &state;
    llhttp_errno_t error = llhttp_execute(&parser, buffer, length);
    if (error != HPE_OK || llhttp_finish(&parser) != HPE_OK || !state.headers_complete) {
        fprintf(stderr, "HTTPParserC parse failed: %s\n", llhttp_errno_name(error));
        return 1;
    }
    printf("{\"method\":\"%s\",\"path\":\"%s\",\"version\":\"%u.%u\"}\n",
           llhttp_method_name((llhttp_method_t)llhttp_get_method(&parser)), state.path,
           llhttp_get_http_major(&parser), llhttp_get_http_minor(&parser));
    return 0;
}
