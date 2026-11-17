#include "harness.h"
#include <fstream>
#include <iostream>
#include <iterator>
#include <string>

static std::string json_escape(const std::string& input) {
  const char hex[] = "0123456789abcdef";
  std::string out;
  for (unsigned char ch : input) {
    if (ch == '\\' || ch == '"') { out += '\\'; out += static_cast<char>(ch); }
    else if (ch == '\n') out += "\\n";
    else if (ch == '\r') out += "\\r";
    else if (ch == '\t') out += "\\t";
    else if (ch < 32 || ch > 126) {
      out += "\\u00";
      out += hex[ch >> 4];
      out += hex[ch & 15];
    } else out += static_cast<char>(ch);
  }
  return out;
}

int main(int argc, char** argv) {
  if (argc != 2) return 2;
  std::ifstream input(argv[1], std::ios::binary);
  if (!input) return 3;
  std::string bytes;
  char chunk[4096];
  while (input.read(chunk, sizeof(chunk)) || input.gcount() > 0) {
    bytes.append(chunk, static_cast<std::size_t>(input.gcount()));
    if (bytes.size() > kMaxInputBytes) return 4;
  }
  if (input.bad()) return 4;
  ParseResult result;
  if (!parse_zip(reinterpret_cast<const uint8_t*>(bytes.data()), bytes.size(), result)) return 5;
  std::cout << "{\"entries\":" << result.entries
            << ",\"name\":\"" << json_escape(result.name)
            << "\",\"content\":\"" << json_escape(result.content) << "\"}\n";
}
