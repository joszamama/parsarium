#include "control.h"
#define FIO_HTTP1_PARSER
#include "fio-stl/include.h"
#include <stdio.h>
#include <string.h>

typedef struct {
    fio_buf_info_s method;
    fio_buf_info_s path;
    fio_buf_info_s version;
    fio_buf_info_s host;
    int complete;
} parsed_request;

static void fio_http1_on_complete(void *user) {
    ((parsed_request *)user)->complete = 1;
}
static int fio_http1_on_method(fio_buf_info_s value, void *user) {
    ((parsed_request *)user)->method = value;
    return 0;
}
static int fio_http1_on_url(fio_buf_info_s value, void *user) {
    ((parsed_request *)user)->path = value;
    return 0;
}
static int fio_http1_on_version(fio_buf_info_s value, void *user) {
    ((parsed_request *)user)->version = value;
    return 0;
}
static int fio_http1_on_header(fio_buf_info_s name, fio_buf_info_s value, void *user) {
    if (name.len == 4 && memcmp(name.buf, "host", 4) == 0)
        ((parsed_request *)user)->host = value;
    return 0;
}
static int fio_http1_on_status(size_t number, fio_buf_info_s text, void *user) {
    (void)number; (void)text; (void)user;
    return 0;
}
static int fio_http1_on_header_content_length(fio_buf_info_s name,
                                              fio_buf_info_s value,
                                              size_t length, void *user) {
    (void)name; (void)value; (void)length; (void)user;
    return 0;
}
static int fio_http1_on_expect(void *user) {
    (void)user;
    return 0;
}
static int fio_http1_on_body_chunk(fio_buf_info_s chunk, void *user) {
    (void)chunk; (void)user;
    return 0;
}

static int equals(fio_buf_info_s slice, const char *text) {
    size_t length = strlen(text);
    return slice.len == length && slice.buf != NULL &&
           memcmp(slice.buf, text, length) == 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char bytes[4096];
    size_t length = read_control(argv[1], bytes, sizeof bytes);
    parsed_request parsed = {0};
    fio_http1_parser_s parser = FIO_HTTP1_PARSER_INIT;
    size_t consumed = fio_http1_parse(&parser, FIO_BUF_INFO2(bytes, length), &parsed);
    if (consumed != length || !parsed.complete ||
        !equals(parsed.method, "GET") || !equals(parsed.path, "/parsarium?x=1") ||
        !equals(parsed.version, "HTTP/1.1") || !equals(parsed.host, "example.test")) {
        fprintf(stderr, "facil.io C STL did not parse the control request\n");
        return 3;
    }
    printf("{\"method\":\"%.*s\",\"path\":\"%.*s\",\"version\":\"%.*s\",\"host\":\"%.*s\"}\n",
           (int)parsed.method.len, parsed.method.buf, (int)parsed.path.len, parsed.path.buf,
           (int)parsed.version.len, parsed.version.buf, (int)parsed.host.len, parsed.host.buf);
    return 0;
}
