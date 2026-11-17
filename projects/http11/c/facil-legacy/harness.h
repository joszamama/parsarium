#ifndef PARSARIUM_FACIL_LEGACY_C_HTTP11_HARNESS_H
#define PARSARIUM_FACIL_LEGACY_C_HTTP11_HARNESS_H

#include <stddef.h>
#include <stdint.h>

/* Inputs that are empty or above 1 MiB are rejected before http1_parse runs. */
#define PARSARIUM_HTTP_MAX_INPUT ((size_t)1 << 20)

/* Strings are heap-allocated, NUL-terminated copies of the parser's slices and
 * always carry an explicit length; release them with
 * parsarium_http_result_clear. query and host are NULL when the parser did
 * not report them. host is the parser's lowercased "host" header value. */
struct parsarium_http_result {
    char *method;
    size_t method_len;
    char *path;
    size_t path_len;
    char *query;
    size_t query_len;
    char *version;
    size_t version_len;
    char *host;
    size_t host_len;
};

int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result);
void parsarium_http_result_clear(struct parsarium_http_result *result);

#endif
