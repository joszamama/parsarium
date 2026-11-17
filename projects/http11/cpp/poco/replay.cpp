#include "harness.h"
#include <fstream>
#include <iostream>
#include <iterator>
#include <string>

static std::string json_escape(const std::string& input) {
  const char hex[] = "0123456789abcdef";
  std::string out;
  for (unsigned char ch : input) {
    if (ch == '\\' || ch == '"') { out += '\\'; out += ch; }
    else if (ch < 32) {
      out += "\\u00";
      out += hex[ch >> 4];
      out += hex[ch & 15];
    } else out += ch;
  }
  return out;
}

int main(int argc, char** argv) {
  if (argc != 2) return 2;
  std::ifstream input(argv[1], std::ios::binary);
  if (!input) return 3;
  std::string bytes((std::istreambuf_iterator<char>(input)), std::istreambuf_iterator<char>());
  if (!input.eof() && input.fail()) return 4;
  ParseResult result;
  if (!parse_http_request(reinterpret_cast<const uint8_t*>(bytes.data()), bytes.size(), result)) return 5;
  std::cout << "{\"method\":\"" << json_escape(result.method)
            << "\",\"path\":\"" << json_escape(result.path)
            << "\",\"version\":\"" << json_escape(result.version)
            << "\",\"host\":\"" << json_escape(result.host) << "\"}\n";
}
