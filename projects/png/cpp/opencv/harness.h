#pragma once
#include <cstddef>
#include <cstdint>
struct Result {
    unsigned width, height;
    bool has_first, has_second;
    std::uint8_t first[4], second[4];
};
bool parse_data(const std::uint8_t *data, std::size_t size, Result *result);
