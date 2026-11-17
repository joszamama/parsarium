#include "harness.h"

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    parsarium_mp3_result result;
    parsarium_parse_mp3(data, size, result);
    return 0;
}
