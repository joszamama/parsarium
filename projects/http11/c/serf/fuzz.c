#include "harness.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_http_response result;
    if (parsarium_parse_http_response(data, size, &result)) parsarium_http_response_free(&result);
    return 0;
}
