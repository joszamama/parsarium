#include "control.h"
#include <stdio.h>
#include <string.h>
#include "lib/facil/http/parsers/http1_parser.h"

typedef struct {
    char *text;
    size_t length;
} slice;

typedef struct {
    http1_parser_s parser;
    slice method, path, query, version, host;
    int complete, error;
} parsed_request;

static parsed_request *result(http1_parser_s *parser) {
    return (parsed_request *)parser;
}
static int http1_on_request(http1_parser_s *parser) {
    result(parser)->complete = 1;
    return 0;
}
static int http1_on_response(http1_parser_s *parser) {
    (void)parser;
    return 0;
}
static int http1_on_method(http1_parser_s *parser, char *text, size_t length) {
    result(parser)->method = (slice){text, length};
    return 0;
}
static int http1_on_status(http1_parser_s *parser, size_t status,
                           char *text, size_t length) {
    (void)parser; (void)status; (void)text; (void)length;
    return 0;
}
static int http1_on_path(http1_parser_s *parser, char *text, size_t length) {
    result(parser)->path = (slice){text, length};
    return 0;
}
static int http1_on_query(http1_parser_s *parser, char *text, size_t length) {
    result(parser)->query = (slice){text, length};
    return 0;
}
static int http1_on_version(http1_parser_s *parser, char *text, size_t length) {
    result(parser)->version = (slice){text, length};
    return 0;
}
static int http1_on_header(http1_parser_s *parser, char *name, size_t name_length,
                           char *value, size_t value_length) {
    if (name_length == 4 && memcmp(name, "host", 4) == 0)
        result(parser)->host = (slice){value, value_length};
    return 0;
}
static int http1_on_body_chunk(http1_parser_s *parser, char *text, size_t length) {
    (void)parser; (void)text; (void)length;
    return 0;
}
static int http1_on_error(http1_parser_s *parser) {
    result(parser)->error = 1;
    return 0;
}
static int equals(slice value, const char *text) {
    size_t length = strlen(text);
    return value.text != NULL && value.length == length &&
           memcmp(value.text, text, length) == 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char bytes[4096];
    size_t length = read_control(argv[1], bytes, sizeof bytes);
    parsed_request parsed = {0};
    size_t consumed = http1_parse(&parsed.parser, bytes, length);
    if (consumed != length || parsed.error || !parsed.complete ||
        !equals(parsed.method, "GET") || !equals(parsed.path, "/parsarium") ||
        !equals(parsed.query, "x=1") || !equals(parsed.version, "HTTP/1.1") ||
        !equals(parsed.host, "example.test")) {
        fprintf(stderr, "facil.io 0.7 did not parse the control request\n");
        return 3;
    }
    printf("{\"method\":\"%.*s\",\"path\":\"%.*s\",\"query\":\"%.*s\",\"version\":\"%.*s\",\"host\":\"%.*s\"}\n",
           (int)parsed.method.length, parsed.method.text,
           (int)parsed.path.length, parsed.path.text,
           (int)parsed.query.length, parsed.query.text,
           (int)parsed.version.length, parsed.version.text,
           (int)parsed.host.length, parsed.host.text);
    return 0;
}
