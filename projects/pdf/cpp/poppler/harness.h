#pragma once
#include <cstddef>
#include <cstdint>
struct Result { int pages; };
bool parse_data(const std::uint8_t *data, std::size_t size, Result *result);
