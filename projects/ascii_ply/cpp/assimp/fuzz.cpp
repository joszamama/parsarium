#include "harness.h"

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    ParsariumPlyResult result{};
    parsarium_parse_ply(data, size, &result);
    return 0;
}
