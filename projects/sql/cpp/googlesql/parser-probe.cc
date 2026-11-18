// Parser-only probe: googlesql::ParseNextStatement over the local bytes; no printing.
#define PARSARIUM_PROBE
#include "googlesql/parsarium/harness.cc"

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  FILE *file = std::fopen(argv[1], "rb");
  if (!file) return 2;
  std::vector<char> data(1u << 20);
  size_t size = std::fread(data.data(), 1, data.size(), file);
  std::fclose(file);
  if (size == 0 || size == data.size()) return 2;
  return ParseAll(std::string(data.data(), size), nullptr);
}
