#ifndef PARSARIUM_LIBMICROHTTPD_C_HTTP11_HARNESS_H
#define PARSARIUM_LIBMICROHTTPD_C_HTTP11_HARNESS_H

#include <stddef.h>
#include <stdint.h>

/* Harness caps, applied before or around libmicrohttpd:
 * - inputs above 1 MiB are rejected before a connection is created;
 * - one exchange (write, half-close, wait for MHD to close) is bounded by
 *   PARSARIUM_HTTP_EXCHANGE_TIMEOUT_MS, and MHD drops idle connections after
 *   two seconds (MHD_OPTION_CONNECTION_TIMEOUT);
 * - the captured method, path and version together may hold at most
 *   PARSARIUM_HTTP_MAX_CAPTURE bytes. MHD's default 32 KiB per-connection
 *   memory pool already bounds a parsed request head below that. */
#define PARSARIUM_HTTP_MAX_INPUT ((size_t)1 << 20)
#define PARSARIUM_HTTP_EXCHANGE_TIMEOUT_MS 5000
#define PARSARIUM_HTTP_MAX_CAPTURE ((size_t)64 * 1024)

/* Strings are heap-allocated, NUL-terminated and sized to the parsed value;
 * release them with parsarium_http_result_clear. path is MHD's URL followed by
 * "?" and the parsed GET arguments rejoined in parser order, when present. */
struct parsarium_http_result {
    char *method;
    size_t method_len;
    char *path;
    size_t path_len;
    char *version;
    size_t version_len;
};

int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result);
void parsarium_http_result_clear(struct parsarium_http_result *result);

/* Stops the shared daemon. Registered with atexit on first use; safe to call
 * more than once. */
void parsarium_http_shutdown(void);

#endif
