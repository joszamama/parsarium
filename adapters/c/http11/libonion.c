#include "control.h"
#include <onion/request.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char bytes[4096];
    size_t length = read_control(argv[1], bytes, sizeof bytes);
    onion_request *request = onion_request_new(NULL);
    if (request == NULL) return 3;
    onion_connection_status status = onion_request_write(request, bytes, length);
    const char *path = onion_request_get_fullpath(request);
    const char *query = onion_request_get_query(request, "x");
    const char *host = onion_request_get_header(request, "Host");
    onion_request_flags flags = onion_request_get_flags(request);
    if (status != OCS_REQUEST_READY || path == NULL || query == NULL || host == NULL ||
        (flags & OR_METHODS) != OR_GET || !(flags & OR_HTTP11) ||
        strcmp(path, "/parsarium") || strcmp(query, "1") || strcmp(host, "example.test")) {
        fprintf(stderr, "libonion did not parse the control request\n");
        onion_request_free(request);
        return 4;
    }
    printf("{\"method\":\"GET\",\"path\":\"%s\",\"version\":\"1.1\",\"host\":\"%s\",\"query_x\":\"%s\"}\n", path, host, query);
    onion_request_free(request);
    return 0;
}
