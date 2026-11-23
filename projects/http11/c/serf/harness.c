#include "harness.h"
#include <apr_general.h>
#include <apr_errno.h>
#include <apr_pools.h>
#include <serf.h>
#include <serf_bucket_types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Inputs above 1 MiB are rejected before Serf sees them. */
#define INPUT_LIMIT ((size_t)1 << 20)
/* Content-Encoding: gzip/deflate bodies are inflated by Serf; cap the output. */
#define BODY_LIMIT ((size_t)4 << 20)
/* A simple bucket always has its bytes available, so the response bucket must
 * make progress; this bounds harness loops if it ever stops doing so. */
#define IDLE_READ_LIMIT 64

static int apr_ready(void) {
    static int state = 0;
    if (!state) state = apr_initialize() == APR_SUCCESS ? 1 : -1;
    return state == 1;
}

/* serf_error_string() lives in Serf's context.c, which is not built here; the
 * response bucket returns these serf.h codes, so they are named directly. */
static const char *serf_status_name(apr_status_t status) {
    switch (status) {
    case SERF_ERROR_CLOSING: return "SERF_ERROR_CLOSING";
    case SERF_ERROR_REQUEST_LOST: return "SERF_ERROR_REQUEST_LOST";
    case SERF_ERROR_WAIT_CONN: return "SERF_ERROR_WAIT_CONN";
    case SERF_ERROR_DECOMPRESSION_FAILED: return "SERF_ERROR_DECOMPRESSION_FAILED";
    case SERF_ERROR_BAD_HTTP_RESPONSE: return "SERF_ERROR_BAD_HTTP_RESPONSE";
    case SERF_ERROR_TRUNCATED_HTTP_RESPONSE: return "SERF_ERROR_TRUNCATED_HTTP_RESPONSE";
    case SERF_ERROR_ABORTED_CONNECTION: return "SERF_ERROR_ABORTED_CONNECTION";
    default: return NULL;
    }
}

static void set_error(struct parsarium_http_response *result, const char *call,
                      apr_status_t status) {
    char text[120];
    const char *name = serf_status_name(status);
    if (!name) name = apr_strerror(status, text, sizeof(text));
    snprintf(result->error, sizeof(result->error), "%s returned %s (status %d)", call, name,
             (int)status);
}

/* Serf returns NUL-terminated strings owned by the bucket allocator; copy them
 * out before the pool is destroyed. */
static char *copy_string(const char *text, size_t *length) {
    size_t n = text ? strlen(text) : 0;
    char *copy = malloc(n + 1);
    if (!copy) return NULL;
    if (n) memcpy(copy, text, n);
    copy[n] = 0;
    *length = n;
    return copy;
}

static int append_body(struct parsarium_http_response *result, size_t *capacity,
                       const char *chunk, apr_size_t length) {
    if (length > BODY_LIMIT - result->body_len) return 0;
    size_t needed = result->body_len + length;
    if (needed + 1 > *capacity) {
        size_t next = *capacity ? *capacity : 256;
        while (next < needed + 1) next *= 2;
        char *grown = realloc(result->body, next);
        if (!grown) return 0;
        result->body = grown;
        *capacity = next;
    }
    memcpy(result->body + result->body_len, chunk, length);
    result->body_len = needed;
    result->body[needed] = 0;
    return 1;
}

/* Serf 1.3 reads a response from a bucket stream: serf_bucket_simple_create
 * wraps the local bytes, serf_bucket_response_create runs the HTTP/1 status
 * line, header, and body (Content-Length, chunked, close-delimited,
 * gzip/deflate) state machine over it. */
static int parse(serf_bucket_alloc_t *allocator, const uint8_t *data, size_t size,
                 struct parsarium_http_response *result) {
    serf_bucket_t *stream = serf_bucket_simple_create((const char *)data, size,
                                                      NULL, NULL, allocator);
    serf_bucket_t *response = serf_bucket_response_create(stream, allocator);
    int ok = 0;
    serf_status_line line = {0};
    apr_status_t status = serf_bucket_response_status(response, &line);
    /* A 101 status line moves the machine straight to its done state, so the
     * first call reports no status line; the second returns the stored one. */
    if (!SERF_BUCKET_READ_ERROR(status) && line.version == 0)
        status = serf_bucket_response_status(response, &line);
    if (SERF_BUCKET_READ_ERROR(status) || line.version == 0) {
        set_error(result, "serf_bucket_response_status", status);
        goto done;
    }
    status = serf_bucket_response_wait_for_headers(response);
    /* When the blank line ends the input, the machine reaches the body state
     * but still reports the stream's EOF; asking again confirms it. */
    if (APR_STATUS_IS_EOF(status))
        status = serf_bucket_response_wait_for_headers(response);
    /* Serf hands everything after a 101 status line to the body unparsed. */
    if (!(status == APR_SUCCESS || (line.code == 101 && APR_STATUS_IS_EOF(status)))) {
        set_error(result, "serf_bucket_response_wait_for_headers", status);
        goto done;
    }
    result->major = SERF_HTTP_VERSION_MAJOR(line.version);
    result->minor = SERF_HTTP_VERSION_MINOR(line.version);
    result->status = line.code;
    result->reason = copy_string(line.reason, &result->reason_len);
    if (!result->reason) goto done;
    const char *type = serf_bucket_headers_get(serf_bucket_response_get_headers(response),
                                               "Content-Type");
    result->has_content_type = type != NULL;
    result->content_type = copy_string(type, &result->content_type_len);
    if (!result->content_type) goto done;
    size_t capacity = 0;
    int idle = 0;
    for (;;) {
        const char *chunk = NULL;
        apr_size_t length = 0;
        status = serf_bucket_read(response, SERF_READ_ALL_AVAIL, &chunk, &length);
        if (SERF_BUCKET_READ_ERROR(status)) {
            set_error(result, "serf_bucket_read", status);
            goto done;
        }
        if (length) {
            if (!chunk || !append_body(result, &capacity, chunk, length)) {
                snprintf(result->error, sizeof(result->error),
                         "body over the harness limit of %zu bytes or out of memory",
                         (size_t)BODY_LIMIT);
                goto done;
            }
            idle = 0;
        } else if (++idle > IDLE_READ_LIMIT) {
            snprintf(result->error, sizeof(result->error),
                     "serf_bucket_read made no progress in %d reads", IDLE_READ_LIMIT);
            goto done;
        }
        if (APR_STATUS_IS_EOF(status)) break;
    }
    if (!result->body) {
        result->body = calloc(1, 1);
        if (!result->body) goto done;
    }
    ok = 1;
done:
    serf_bucket_destroy(response);
    return ok;
}

int parsarium_parse_http_response(const uint8_t *data, size_t size,
                                  struct parsarium_http_response *result) {
    if (!result) return 0;
    memset(result, 0, sizeof(*result));
    if (!data || !size || size > INPUT_LIMIT) {
        snprintf(result->error, sizeof(result->error), "input outside harness limit");
        return 0;
    }
    apr_pool_t *pool = NULL;
    if (!apr_ready() || apr_pool_create(&pool, NULL) != APR_SUCCESS) {
        snprintf(result->error, sizeof(result->error), "APR initialization failed");
        return 0;
    }
    serf_bucket_alloc_t *allocator = serf_bucket_allocator_create(pool, NULL, NULL);
    int ok = parse(allocator, data, size, result);
    apr_pool_destroy(pool);
    if (!ok) parsarium_http_response_free(result);
    return ok;
}

void parsarium_http_response_free(struct parsarium_http_response *result) {
    if (!result) return;
    free(result->reason);
    free(result->content_type);
    free(result->body);
    result->reason = result->content_type = result->body = NULL;
    result->reason_len = result->content_type_len = result->body_len = 0;
}
