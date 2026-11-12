#include "control.h"
#include <apr_general.h>
#include <apr_pools.h>
#include <serf.h>
#include <serf_bucket_types.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char bytes[4096];
    size_t length = read_control(argv[1], bytes, sizeof bytes);
    if (apr_initialize() != APR_SUCCESS) return 3;
    apr_pool_t *pool = NULL;
    if (apr_pool_create(&pool, NULL) != APR_SUCCESS) return 4;
    serf_bucket_alloc_t *allocator = serf_bucket_allocator_create(pool, NULL, NULL);
    serf_bucket_t *stream = serf_bucket_simple_create(bytes, length, NULL, NULL, allocator);
    serf_bucket_t *response = serf_bucket_response_create(stream, allocator);
    serf_status_line status_line{};
    apr_status_t status = serf_bucket_response_status(response, &status_line);
    apr_status_t headers_status = serf_bucket_response_wait_for_headers(response);
    serf_bucket_t *headers = serf_bucket_response_get_headers(response);
    const char *content_type = headers ? serf_bucket_headers_get(headers, "Content-Type") : NULL;
    const char *content_length = headers ? serf_bucket_headers_get(headers, "Content-Length") : NULL;
    const char *body = NULL;
    apr_size_t body_length = 0;
    apr_status_t body_status = serf_bucket_read(response, SERF_READ_ALL_AVAIL, &body, &body_length);
    if (status != APR_SUCCESS || headers_status != APR_SUCCESS ||
        status_line.version != SERF_HTTP_11 || status_line.code != 200 ||
        status_line.reason == NULL || strcmp(status_line.reason, "OK") ||
        content_type == NULL || strcmp(content_type, "text/plain") ||
        content_length == NULL || strcmp(content_length, "2") ||
        !(body_status == APR_SUCCESS || APR_STATUS_IS_EOF(body_status)) ||
        body_length != 2 || body == NULL || memcmp(body, "OK", 2)) {
        fprintf(stderr, "Apache Serf did not parse the response control\n");
        serf_bucket_destroy(response);
        apr_pool_destroy(pool);
        apr_terminate();
        return 5;
    }
    printf("{\"version\":\"1.1\",\"status\":200,\"reason\":\"%s\",\"content_type\":\"%s\",\"body\":\"OK\"}\n",
           status_line.reason, content_type);
    serf_bucket_destroy(response);
    apr_pool_destroy(pool);
    apr_terminate();
    return 0;
}
