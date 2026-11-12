#define HTTPP_IMPLEMENTATION
#include <httpp.h>
#include <stdio.h>
#include "control.h"

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: httpp control.http\n"); return 1; }
    char buffer[4096];
    size_t length = read_control(argv[1], buffer, sizeof(buffer));
    httpp_req_t request;
    httpp_header_t headers[HTTPP_DEFAULT_HEADERS_ARR_CAP];
    httpp_init_req(&request, headers, HTTPP_DEFAULT_HEADERS_ARR_CAP);
    if (httpp_parse_request(buffer, length, &request) < 0) {
        fprintf(stderr, "httpp parse failed\n");
        return 1;
    }
    if (request.version.length < 5) return 1;
    printf("{\"method\":\"%s\",\"path\":\"%.*s\",\"version\":\"%.*s\"}\n",
           httpp_method_to_string(request.method),
           (int)request.route.length, request.route.ptr,
           (int)(request.version.length - 5), request.version.ptr + 5);
    return 0;
}
