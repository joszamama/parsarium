#include "harness.h"

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    int pages = -1;
    parsarium_parse_pdf(data, size, pages);
    return 0;
}
