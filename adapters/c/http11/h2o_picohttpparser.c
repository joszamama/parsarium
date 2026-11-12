/* H2O 2.2.6 vendors PicoHTTPParser; this adapter uses that tagged H2O copy. */
#include <picohttpparser.h>
#include <stdio.h>
#include "control.h"

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: h2o-picohttpparser control.http\n"); return 1; }
    char buffer[4096];
    size_t length = read_control(argv[1], buffer, sizeof(buffer));
    const char *method, *path;
    size_t method_length, path_length;
    int minor;
    struct phr_header headers[32];
    size_t header_count = sizeof(headers) / sizeof(headers[0]);
    int consumed = phr_parse_request(buffer, length, &method, &method_length, &path,
                                     &path_length, &minor, headers, &header_count, 0);
    if (consumed != (int)length || minor != 1) {
        fprintf(stderr, "picohttpparser parse failed\n");
        return 1;
    }
    printf("{\"method\":\"%.*s\",\"path\":\"%.*s\",\"version\":\"1.%d\"}\n",
           (int)method_length, method, (int)path_length, path, minor);
    return 0;
}
