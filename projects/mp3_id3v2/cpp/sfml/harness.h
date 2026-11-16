#pragma once
#include <cstddef>
#include <cstdint>
struct Result { unsigned sample_rate, channels; std::uint64_t frames, samples; std::int16_t first[4]; unsigned decoded_samples; };
bool parse_data(const std::uint8_t *data, std::size_t size, Result *result);
