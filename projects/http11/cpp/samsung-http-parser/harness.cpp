#include "harness.h"
#include <http_parser.h>
#include <string.h>

struct state { struct parsarium_http_result *result; size_t path_length; int headers_complete; };
static int on_url(http_parser *parser, const char *bytes, size_t length) {
    struct state *state = (struct state *)parser->data;
    if (state->path_length + length >= sizeof(state->result->path)) return -1;
    memcpy(state->result->path + state->path_length, bytes, length);
    state->path_length += length;
    state->result->path[state->path_length] = 0;
    return 0;
}
static int on_headers_complete(http_parser *parser) {
    ((struct state *)parser->data)->headers_complete = 1;
    return 0;
}
int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    struct state state = {result, 0, 0};
    http_parser parser;
    http_parser_settings settings;
    http_parser_init(&parser, HTTP_REQUEST);
    parser.data = &state;
    http_parser_settings_init(&settings);
    settings.on_url = on_url;
    settings.on_headers_complete = on_headers_complete;
    size_t consumed = http_parser_execute(&parser, &settings, (const char *)data, size);
    if (consumed != size || HTTP_PARSER_ERRNO(&parser) != HPE_OK ||
        !state.headers_complete || !state.path_length) return 0;
    const char *method = http_method_str((enum http_method)parser.method);
    if (strlen(method) >= sizeof(result->method)) return 0;
    strcpy(result->method, method);
    result->major = parser.http_major;
    result->minor = parser.http_minor;
    return 1;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_http_result result;
    (void)parsarium_parse_http(data, size, &result);
    return 0;
}
