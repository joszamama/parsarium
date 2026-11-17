#pragma once
#include <cstddef>
#include <cstdint>
#include <string>

struct ParseResult {
  std::string method;
  std::string path;
  std::string version;
  std::string host;
};

bool parse_http_request(const uint8_t* data, std::size_t size, ParseResult& out);
