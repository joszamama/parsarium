#include "harness.h"

#include <stdlib.h>
#include <string.h>

/* facil.io 0.7.6 ships its HTTP/1 parser as one header: http1_parse and its
 * stages are static functions compiled into this translation unit, and the
 * including file supplies the callbacks below. The header's defaults are kept
 * (lowercased header names, memchr-based seeking, no EOL-to-NUL rewrite). */
#include "lib/facil/http/parsers/http1_parser.h"

struct slice {
    const char *text;
    size_t length;
};

/* The parser state is the first member, so a callback's http1_parser_s
 * pointer is also a pointer to its request context. */
struct request {
    http1_parser_s parser;
    struct slice method, path, query, version, host;
    int has_query, host_count, complete, response, error;
};

static struct request *request_of(http1_parser_s *parser) {
    return (struct request *)parser;
}

static int http1_on_request(http1_parser_s *parser) {
    request_of(parser)->complete = 1;
    return 0;
}

static int http1_on_response(http1_parser_s *parser) {
    /* The catalog scope is requests; a status line is not a result. */
    request_of(parser)->response = 1;
    return 0;
}

static int http1_on_method(http1_parser_s *parser, char *method, size_t method_len) {
    request_of(parser)->method = (struct slice){method, method_len};
    return 0;
}

static int http1_on_status(http1_parser_s *parser, size_t status, char *status_str,
                           size_t len) {
    (void)status;
    (void)status_str;
    (void)len;
    request_of(parser)->response = 1;
    return 0;
}

static int http1_on_path(http1_parser_s *parser, char *path, size_t path_len) {
    request_of(parser)->path = (struct slice){path, path_len};
    return 0;
}

static int http1_on_query(http1_parser_s *parser, char *query, size_t query_len) {
    struct request *request = request_of(parser);
    request->query = (struct slice){query, query_len};
    request->has_query = 1;
    return 0;
}

static int http1_on_version(http1_parser_s *parser, char *version, size_t len) {
    request_of(parser)->version = (struct slice){version, len};
    return 0;
}

static int http1_on_header(http1_parser_s *parser, char *name, size_t name_len,
                           char *data, size_t data_len) {
    struct request *request = request_of(parser);
    /* Names arrive lowercased (HTTP_HEADERS_LOWERCASE). An absolute-form
     * request target is also reported as a "host" header by the parser. */
    if (name_len == 4 && memcmp(name, "host", 4) == 0) {
        request->host = (struct slice){data, data_len};
        request->host_count++;
    }
    return 0;
}

static int http1_on_body_chunk(http1_parser_s *parser, char *data, size_t data_len) {
    (void)parser;
    (void)data;
    (void)data_len;
    return 0;
}

static int http1_on_error(http1_parser_s *parser) {
    request_of(parser)->error = 1;
    return 0;
}

static int copy_slice(struct slice value, char **text, size_t *length) {
    char *copy = malloc(value.length + 1);
    if (!copy) return 0;
    if (value.length) memcpy(copy, value.text, value.length);
    copy[value.length] = '\0';
    *text = copy;
    *length = value.length;
    return 1;
}

int parsarium_parse_http(const uint8_t *data, size_t size,
                         struct parsarium_http_result *result) {
    if (!result) return 0;
    memset(result, 0, sizeof(*result));
    if (!data || size == 0 || size > PARSARIUM_HTTP_MAX_INPUT) return 0;
    /* http1_parse takes writable bytes (it lowercases header names in place).
     * The copy is exactly the input length, so any parser read or write past
     * the caller's bytes is reported by AddressSanitizer. */
    char *bytes = malloc(size);
    if (!bytes) return 0;
    memcpy(bytes, data, size);

    struct request request;
    memset(&request, 0, sizeof(request));
    request.parser = (http1_parser_s)HTTP1_PARSER_INIT;
    size_t consumed = http1_parse(&request.parser, bytes, size);

    /* One complete request must consume every input byte. A repeated Host
     * value is ambiguous, so it is not reported as a result. */
    int ok = consumed == size && request.complete && !request.error && !request.response &&
             request.method.text && request.path.text && request.version.text &&
             request.host_count <= 1;
    if (ok) {
        ok = copy_slice(request.method, &result->method, &result->method_len) &&
             copy_slice(request.path, &result->path, &result->path_len) &&
             copy_slice(request.version, &result->version, &result->version_len) &&
             (!request.has_query ||
              copy_slice(request.query, &result->query, &result->query_len)) &&
             (!request.host_count ||
              copy_slice(request.host, &result->host, &result->host_len));
        if (!ok) parsarium_http_result_clear(result);
    }
    free(bytes);
    return ok;
}

void parsarium_http_result_clear(struct parsarium_http_result *result) {
    if (!result) return;
    free(result->method);
    free(result->path);
    free(result->query);
    free(result->version);
    free(result->host);
    memset(result, 0, sizeof(*result));
}
