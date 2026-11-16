#ifndef PARSARIUM_LIBZIPPP_HARNESS_HPP
#define PARSARIUM_LIBZIPPP_HARNESS_HPP
#include <cstddef>
#include <cstdint>
struct parsarium_zip_result { std::size_t entries,name_len,content_len; char name[256],content[4096]; };
bool parsarium_parse_zip(const std::uint8_t *data,std::size_t size,parsarium_zip_result *result);
#endif
