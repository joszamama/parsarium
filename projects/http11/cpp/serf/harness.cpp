#include "harness.h"

#include <apr_errno.h>
#include <apr_general.h>
#include <apr_pools.h>
#include <serf.h>
#include <serf_bucket_types.h>

#include <string>

namespace {

constexpr std::size_t input_limit = 1u << 20;
// Content-Encoding: gzip/deflate bodies are inflated by Serf; cap the output.
constexpr std::size_t body_limit = 4u << 20;
// A simple bucket always has its bytes available, so the response bucket must
// make progress; this bounds harness loops if it ever stops doing so.
constexpr int idle_read_limit = 64;

bool apr_ready() {
    static const bool ready = apr_initialize() == APR_SUCCESS;
    return ready;
}

// serf_error_string() lives in Serf's context.c, which is not built here; the
// response bucket returns these serf.h codes, so they are named directly.
const char *serf_status_name(apr_status_t status) {
    switch (status) {
    case SERF_ERROR_CLOSING: return "SERF_ERROR_CLOSING";
    case SERF_ERROR_REQUEST_LOST: return "SERF_ERROR_REQUEST_LOST";
    case SERF_ERROR_WAIT_CONN: return "SERF_ERROR_WAIT_CONN";
    case SERF_ERROR_DECOMPRESSION_FAILED: return "SERF_ERROR_DECOMPRESSION_FAILED";
    case SERF_ERROR_BAD_HTTP_RESPONSE: return "SERF_ERROR_BAD_HTTP_RESPONSE";
    case SERF_ERROR_TRUNCATED_HTTP_RESPONSE: return "SERF_ERROR_TRUNCATED_HTTP_RESPONSE";
    case SERF_ERROR_ABORTED_CONNECTION: return "SERF_ERROR_ABORTED_CONNECTION";
    default: return nullptr;
    }
}

std::string status_error(const char *call, apr_status_t status) {
    char text[120];
    const char *name = serf_status_name(status);
    if (!name) name = apr_strerror(status, text, sizeof(text));
    return std::string(call) + " returned " + name + " (status " +
           std::to_string(static_cast<int>(status)) + ")";
}

// Serf 1.3 reads a response from a bucket stream: serf_bucket_simple_create
// wraps the local bytes, serf_bucket_response_create runs the HTTP/1 status
// line, header, and body (Content-Length, chunked, close-delimited, gzip/deflate)
// state machine over it.
bool parse(serf_bucket_alloc_t *allocator, const std::uint8_t *data, std::size_t size,
           ParsariumHttpResponse *result) {
    serf_bucket_t *stream = serf_bucket_simple_create(
        reinterpret_cast<const char *>(data), size, nullptr, nullptr, allocator);
    serf_bucket_t *response = serf_bucket_response_create(stream, allocator);
    bool ok = false;

    serf_status_line line{};
    apr_status_t status = serf_bucket_response_status(response, &line);
    // A 101 status line moves the machine straight to its done state, so the
    // first call reports no status line; the second returns the stored one.
    if (!SERF_BUCKET_READ_ERROR(status) && line.version == 0)
        status = serf_bucket_response_status(response, &line);
    if (!SERF_BUCKET_READ_ERROR(status) && line.version != 0) {
        status = serf_bucket_response_wait_for_headers(response);
        // When the blank line ends the input, the machine reaches the body
        // state but still reports the stream's EOF; asking again confirms it.
        if (APR_STATUS_IS_EOF(status))
            status = serf_bucket_response_wait_for_headers(response);
        // Serf hands everything after a 101 status line to the body unparsed.
        bool headers_done = status == APR_SUCCESS ||
                            (line.code == 101 && APR_STATUS_IS_EOF(status));
        if (headers_done) {
            result->major = SERF_HTTP_VERSION_MAJOR(line.version);
            result->minor = SERF_HTTP_VERSION_MINOR(line.version);
            result->status = line.code;
            result->reason = line.reason ? line.reason : "";
            const char *type =
                serf_bucket_headers_get(serf_bucket_response_get_headers(response),
                                        "Content-Type");
            result->has_content_type = type != nullptr;
            result->content_type = type ? type : "";
            ok = true;
            int idle = 0;
            for (;;) {
                const char *chunk = nullptr;
                apr_size_t length = 0;
                status = serf_bucket_read(response, SERF_READ_ALL_AVAIL, &chunk, &length);
                if (SERF_BUCKET_READ_ERROR(status)) {
                    result->error = status_error("serf_bucket_read", status);
                    ok = false;
                    break;
                }
                if (length) {
                    if (result->body.size() + length > body_limit) {
                        result->error = "body over the harness limit of " +
                                        std::to_string(body_limit) + " bytes";
                        ok = false;
                        break;
                    }
                    result->body.append(chunk, length);
                    idle = 0;
                } else if (++idle > idle_read_limit) {
                    result->error = "serf_bucket_read made no progress in " +
                                    std::to_string(idle_read_limit) + " reads";
                    ok = false;
                    break;
                }
                if (APR_STATUS_IS_EOF(status)) break;
            }
        } else {
            result->error = status_error("serf_bucket_response_wait_for_headers", status);
        }
    } else {
        result->error = status_error("serf_bucket_response_status", status);
    }
    serf_bucket_destroy(response);
    return ok;
}

}  // namespace

bool parsarium_parse_http_response(const std::uint8_t *data, std::size_t size,
                                   ParsariumHttpResponse *result) {
    if (!result) return false;
    if (!data || size == 0 || size > input_limit) {
        result->error = "input outside harness limit";
        return false;
    }
    apr_pool_t *pool = nullptr;
    if (!apr_ready() || apr_pool_create(&pool, nullptr) != APR_SUCCESS) {
        result->error = "APR initialization failed";
        return false;
    }
    serf_bucket_alloc_t *allocator = serf_bucket_allocator_create(pool, nullptr, nullptr);
    bool ok = parse(allocator, data, size, result);
    apr_pool_destroy(pool);
    return ok;
}
