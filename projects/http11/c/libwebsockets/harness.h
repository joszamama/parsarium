#ifndef PARSARIUM_LIBWEBSOCKETS_C_HTTP11_HARNESS_H
#define PARSARIUM_LIBWEBSOCKETS_C_HTTP11_HARNESS_H

#include <stddef.h>
#include <stdint.h>

/* The documented adopt-readbuf API accepts at most 2048 initial bytes.
 * Larger inputs are rejected before lws sees them. */
#define PARSARIUM_HTTP_MAX_INPUT ((size_t)2048)

/* Strings are heap-allocated, NUL-terminated and sized to the parsed value;
 * release them with parsarium_http_result_clear. An absent Host header or
 * query yields an empty string, matching projects/http11/cpp/libwebsockets. */
struct parsarium_http_result {
    char *method;
    char *path; /* urldecoded path, then "?" and the '&'-joined query args */
    char *host;
};

int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result);
void parsarium_http_result_clear(struct parsarium_http_result *result);

/* Destroys the shared lws context. Optional: replay calls it before exit so
 * every lws allocation is released; the fuzzer keeps the context alive. */
void parsarium_http_teardown(void);

#endif
