#pragma once
#include <cstddef>
#include <cstdint>
struct Result { size_t pages, width, height; };
int parse_data(const uint8_t *data, size_t size, Result *result);
