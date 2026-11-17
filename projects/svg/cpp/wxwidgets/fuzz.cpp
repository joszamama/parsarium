#include "harness.h"

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    parsarium_svg_result result{};
    parsarium_parse_svg(data, size, &result);
    return 0;
}
