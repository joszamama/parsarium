#ifndef PARSARIUM_WX_PNM_H
#define PARSARIUM_WX_PNM_H

#include <cstddef>
#include <cstdint>

struct parsarium_pnm_result {
    int width;
    int height;
    unsigned char first[4];
    unsigned char second[4];
    bool second_present;
};

bool parsarium_parse_pnm(const std::uint8_t *data, std::size_t size,
                         parsarium_pnm_result *result);

#endif
