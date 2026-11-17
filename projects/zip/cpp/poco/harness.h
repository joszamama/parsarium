#pragma once
#include <cstddef>
#include <cstdint>
#include <string>

// Harness caps: input at most 1 MiB, entry name at most 64 KiB (the ZIP
// field limit), decompressed content of the first entry at most 1 MiB.
constexpr std::size_t kMaxInputBytes = 1u << 20;
constexpr std::size_t kMaxNameBytes = 1u << 16;
constexpr std::size_t kMaxContentBytes = 1u << 20;

struct ParseResult {
  std::size_t entries = 0;
  std::string name;
  std::string content;
};

bool parse_zip(const uint8_t* data, std::size_t size, ParseResult& out);
