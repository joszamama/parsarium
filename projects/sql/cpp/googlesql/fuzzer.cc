// libFuzzer entry for the coverage image: googlesql::ParseNextStatement over the input bytes.
#define PARSARIUM_PROBE
#include "googlesql/parsarium/harness.cc"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  ParseAll(std::string(reinterpret_cast<const char *>(data), size), nullptr);
  return 0;
}
