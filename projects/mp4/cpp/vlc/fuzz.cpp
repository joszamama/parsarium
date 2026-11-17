#include "harness.h"

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    parsarium_mp4_result result;
    parsarium_parse_mp4(data, size, result);
    return 0;
}
