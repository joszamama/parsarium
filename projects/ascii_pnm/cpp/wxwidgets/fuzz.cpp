#include "harness.h"

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    parsarium_pnm_result result{};
    parsarium_parse_pnm(data, size, &result);
    return 0;
}
