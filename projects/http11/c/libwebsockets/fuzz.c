#include "harness.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_http_result result;
    if (parsarium_parse_http(data, size, &result)) parsarium_http_result_clear(&result);
    return 0;
}
