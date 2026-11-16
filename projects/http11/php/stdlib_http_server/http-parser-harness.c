#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "php_http_parser.h"

typedef struct {
    char target[4096];
    char field[256];
    char host[256];
    char custom[256];
    int value_started;
    int headers_complete;
} request_observation;

static void append(char *destination, size_t capacity, const char *source, size_t length) {
    size_t used = strlen(destination);
    if (used < capacity - 1) {
        size_t available = capacity - used - 1;
        if (length > available) length = available;
        memcpy(destination + used, source, length);
        destination[used + length] = '\0';
    }
}

static int on_url(php_http_parser *parser, const char *data, size_t length) {
    request_observation *result = parser->data;
    append(result->target, sizeof(result->target), data, length);
    return 0;
}

static int on_header_field(php_http_parser *parser, const char *data, size_t length) {
    request_observation *result = parser->data;
    if (result->value_started) {
        result->field[0] = '\0';
        result->value_started = 0;
    }
    append(result->field, sizeof(result->field), data, length);
    return 0;
}

static int on_header_value(php_http_parser *parser, const char *data, size_t length) {
    request_observation *result = parser->data;
    result->value_started = 1;
    if (strcasecmp(result->field, "Host") == 0) {
        append(result->host, sizeof(result->host), data, length);
    } else if (strcasecmp(result->field, "X-Parsarium") == 0) {
        append(result->custom, sizeof(result->custom), data, length);
    }
    return 0;
}

static int on_headers_complete(php_http_parser *parser) {
    request_observation *result = parser->data;
    result->headers_complete = 1;
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *input = fopen(argv[1], "rb");
    if (!input) return 0;
    if (fseek(input, 0, SEEK_END) || ftell(input) < 0 || ftell(input) > (1 << 20)) {
        fclose(input);
        return 0;
    }
    size_t length = (size_t)ftell(input);
    rewind(input);
    char *bytes = malloc(length ? length : 1);
    if (!bytes) {
        fclose(input);
        return 0;
    }
    if (fread(bytes, 1, length, input) != length) {
        free(bytes);
        fclose(input);
        return 0;
    }
    fclose(input);

    request_observation result = {0};
    php_http_parser parser;
    php_http_parser_settings settings = {0};
    settings.on_url = on_url;
    settings.on_header_field = on_header_field;
    settings.on_header_value = on_header_value;
    settings.on_headers_complete = on_headers_complete;
    php_http_parser_init(&parser, PHP_HTTP_REQUEST);
    parser.data = &result;
    size_t consumed = php_http_parser_execute(&parser, &settings, bytes, length);
    free(bytes);
    if (consumed != length || !result.headers_complete) return 0;
    printf("{\"method\":\"%s\",\"target\":\"%s\",\"version\":\"%u.%u\",\"host\":\"%s\",\"custom\":\"%s\"}\n",
           php_http_method_str(parser.method), result.target, parser.http_major,
           parser.http_minor, result.host, result.custom);
    return 0;
}
