#include "harness.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parsarium_zip_result result{};
    (void)parsarium_parse_zip(data, size, &result);
    return 0;
}
