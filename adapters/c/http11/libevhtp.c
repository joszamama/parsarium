#include <stdint.h>
#include <stddef.h>
#include <htparse.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "control.h"

struct state { char path[256]; char args[128]; int headers_complete; };

static int on_path(htparser *parser, const char *bytes, size_t length) {
    struct state *state = htparser_get_userdata(parser);
    if (length >= sizeof(state->path)) return -1;
    memcpy(state->path, bytes, length);
    state->path[length] = 0;
    return 0;
}

static int on_args(htparser *parser, const char *bytes, size_t length) {
    struct state *state = htparser_get_userdata(parser);
    if (length >= sizeof(state->args)) return -1;
    memcpy(state->args, bytes, length);
    state->args[length] = 0;
    return 0;
}

static int on_headers_complete(htparser *parser) {
    ((struct state *)htparser_get_userdata(parser))->headers_complete = 1;
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: libevhtp control.http\n"); return 1; }
    char buffer[4096];
    size_t length = read_control(argv[1], buffer, sizeof(buffer));
    htparser *parser = htparser_new();
    if (!parser) return 1;
    htparser_init(parser, htp_type_request);
    struct state state = {0};
    htparser_set_userdata(parser, &state);
    htparse_hooks hooks = {0};
    hooks.path = on_path;
    hooks.args = on_args;
    hooks.on_hdrs_complete = on_headers_complete;
    size_t consumed = htparser_run(parser, &hooks, buffer, length);
    if (consumed != length || htparser_get_error(parser) != htparse_error_none ||
        !state.headers_complete) {
        fprintf(stderr, "libevhtp parse failed: %s\n", htparser_get_strerror(parser));
        free(parser);
        return 1;
    }
    printf("{\"method\":\"%s\",\"path\":\"%s%s%s\",\"version\":\"%u.%u\"}\n",
           htparser_get_methodstr(parser), state.path, state.args[0] ? "?" : "", state.args,
           htparser_get_major(parser), htparser_get_minor(parser));
    free(parser);
    return 0;
}
