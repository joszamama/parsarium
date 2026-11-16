#pragma once
#include <cstddef>
#include <cstdint>
struct Result {
    double width, height, frames, fps;
};
bool parse_data(const std::uint8_t *data, std::size_t size, Result *result);
