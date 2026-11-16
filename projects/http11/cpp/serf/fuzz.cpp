#include "harness.h"

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    ParsariumHttpResponse result{};
    parsarium_parse_http_response(data, size, &result);
    return 0;
}
