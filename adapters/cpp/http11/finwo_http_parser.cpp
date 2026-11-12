#include <http-parser.h>
#include <stdio.h>
#include <string.h>
#include "control.h"

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: finwo-http-parser control.http\n"); return 1; }
    char bytes[4096];
    size_t length = read_control(argv[1], bytes, sizeof(bytes));
    struct buf input{}; input.data = bytes; input.len = length; input.cap = length;
    struct http_parser_message *request = http_parser_request_init();
    if (request == NULL) return 1;
    http_parser_request_data(request, &input);
    const char *host = http_parser_header_get(request, "host");
    if (!request->ready || !request->method || !request->path ||
        !request->query || !request->version || !host) {
        fprintf(stderr, "finwo HTTP parse incomplete\n");
        http_parser_message_free(request);
        return 1;
    }
    printf("{\"method\":\"%s\",\"path\":\"%s\",\"query\":\"%s\",\"version\":\"%s\",\"host\":\"%s\"}\n",
           request->method, request->path, request->query, request->version, host);
    http_parser_message_free(request);
    return 0;
}
