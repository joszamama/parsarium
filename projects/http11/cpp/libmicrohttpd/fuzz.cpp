#include "harness.h"

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    ParsariumHttpResult result{};
    parsarium_parse_http(data, size, &result);
    return 0;
}
