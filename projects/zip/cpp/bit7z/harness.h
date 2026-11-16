#pragma once
#include <cstddef>
#include <cstdint>
#include <string>

// Harness caps: input at most 1 MiB and decoded content of the reported entry
// at most 1 MiB. Entry names are bounded by the 64 KiB ZIP name field.
constexpr std::size_t kMaxInputBytes = 1u << 20;
constexpr std::size_t kMaxContentBytes = 1u << 20;

struct ParseResult {
  std::size_t entries = 0;
  std::string name;
  std::string content;
};

bool parse_zip(const uint8_t* data, std::size_t size, ParseResult& out);
