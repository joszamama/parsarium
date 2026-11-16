#pragma once
#include <cstddef>
#include <cstdint>

struct parsarium_pnm_result {
    std::size_t width, height;
    unsigned first[4], second[4];
};

bool parsarium_parse_pnm(const std::uint8_t *data, std::size_t size,
                         parsarium_pnm_result *result);
