#ifndef PARSARIUM_CPP_LIBZIP_HARNESS_HPP
#define PARSARIUM_CPP_LIBZIP_HARNESS_HPP

#include <cstddef>
#include <cstdint>

struct parsarium_zip_result {
    std::int64_t entries;
    char name[256];
    std::size_t name_len;
    unsigned char content[4096];
    std::size_t content_len;
};

bool parsarium_parse_zip(const std::uint8_t *data, std::size_t size,
                         parsarium_zip_result *result);

#endif
