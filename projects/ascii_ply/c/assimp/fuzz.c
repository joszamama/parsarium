#include "harness.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_ply_result result;
    parsarium_parse_ply(data, size, &result);
    return 0;
}
