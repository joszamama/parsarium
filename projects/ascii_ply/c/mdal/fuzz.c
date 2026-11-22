#include "harness.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_ply_result result = {0};
    if (parsarium_parse_ply(data, size, &result)) parsarium_free_result(&result);
    return 0;
}
