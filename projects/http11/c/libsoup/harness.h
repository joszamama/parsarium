#ifndef PARSARIUM_LIBSOUP_C_HTTP11_HARNESS_H
#define PARSARIUM_LIBSOUP_C_HTTP11_HARNESS_H

#include <stddef.h>
#include <stdint.h>

/* Inputs above 1 MiB are rejected before parsing. This is a harness cap that
 * bounds replay and fuzzing work; libsoup itself applies its own 100 KiB
 * request-head limit, which the harness mirrors (see harness.c). */
#define PARSARIUM_HTTP_MAX_INPUT ((size_t)1 << 20)

/* Strings are heap-allocated with GLib and sized to the parsed value; release
 * them with parsarium_http_result_clear. host is NULL when no Host header. */
struct parsarium_http_result {
    char *method;
    char *path;
    int major;
    int minor;
    char *host;
};

int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result);
void parsarium_http_result_clear(struct parsarium_http_result *result);

#endif
