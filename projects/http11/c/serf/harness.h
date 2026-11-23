#ifndef PARSARIUM_SERF_C_HTTP11_HARNESS_H
#define PARSARIUM_SERF_C_HTTP11_HARNESS_H
#include <stddef.h>
#include <stdint.h>
struct parsarium_http_response {
    int major;
    int minor;
    int status;
    char *reason;
    size_t reason_len;
    int has_content_type;
    char *content_type;
    size_t content_type_len;
    char *body;
    size_t body_len;
    /* Why parsing failed: the Serf call and the status it returned. */
    char error[192];
};
int parsarium_parse_http_response(const uint8_t *data, size_t size,
                                  struct parsarium_http_response *result);
void parsarium_http_response_free(struct parsarium_http_response *result);
#endif
