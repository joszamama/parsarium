#include "harness.h"
#include <http_parser.h>
#include <httpdef.h>
#include <stdlib.h>
#include <string.h>

/* libhv 1.3.1 bundles a modified C copy of Node/Joyent http-parser 2.9.1.
 * http_parser_* come from http/http_parser.c; libhv moved http_method_str
 * into http/httpdef.c. */
struct state {
    struct parsarium_http_result *result;
    size_t path_capacity;
    int headers_complete;
    int failed;
};

static int on_url(http_parser *parser, const char *bytes, size_t length) {
    struct state *state = (struct state *)parser->data;
    if (!state || state->failed || state->headers_complete || (!bytes && length)) goto fail;
    if (!length) return 0;
    if (length > state->path_capacity - state->result->path_len) goto fail;
    memcpy(state->result->path + state->result->path_len, bytes, length);
    state->result->path_len += length;
    state->result->path[state->result->path_len] = 0;
    return 0;
fail:
    if (state) state->failed = 1;
    return -1;
}

static int on_headers_complete(http_parser *parser) {
    struct state *state = (struct state *)parser->data;
    if (!state || state->failed || state->headers_complete) {
        if (state) state->failed = 1;
        return -1;
    }
    state->headers_complete = 1;
    return 0;
}

int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    result->path = malloc(size + 1);
    if (!result->path) return 0;
    result->path[0] = 0;
    struct state state = {result, size, 0, 0};
    http_parser parser;
    http_parser_settings settings;
    http_parser_init(&parser, HTTP_REQUEST);
    parser.data = &state;
    http_parser_settings_init(&settings);
    settings.on_url = on_url;
    settings.on_headers_complete = on_headers_complete;
    size_t consumed = http_parser_execute(&parser, &settings, (const char *)data, size);
    if (consumed != size || HTTP_PARSER_ERRNO(&parser) != HPE_OK || state.failed ||
        !state.headers_complete || !result->path_len) {
        parsarium_http_result_free(result);
        return 0;
    }
    const char *method = http_method_str((enum http_method)parser.method);
    size_t method_length = method ? strlen(method) : 0;
    if (!method_length || strcmp(method, "<unknown>") == 0) {
        parsarium_http_result_free(result);
        return 0;
    }
    result->method = method;
    result->method_len = method_length;
    result->major = parser.http_major;
    result->minor = parser.http_minor;
    return 1;
}

void parsarium_http_result_free(struct parsarium_http_result *result) {
    if (!result) return;
    free(result->path);
    result->path = NULL;
    result->path_len = 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_http_result result;
    if (parsarium_parse_http(data, size, &result)) parsarium_http_result_free(&result);
    return 0;
}
