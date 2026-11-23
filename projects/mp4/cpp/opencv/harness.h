#pragma once
#include <cstddef>
#include <cstdint>
#include <string>
struct Result {
    double width, height, frames, fps;
    // OpenCV's reason, or the call that failed, when the file is rejected.
    std::string error;
};
bool parse_data(const std::uint8_t *data, std::size_t size, Result *result);
