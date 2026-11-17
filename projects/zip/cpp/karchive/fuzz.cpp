#include "harness.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
  ParseResult result;
  (void)parse_zip(data, size, result);
  return 0;
}
