#ifndef PARSARIUM_LIBMP4TAG_CPP_HARNESS_H
#define PARSARIUM_LIBMP4TAG_CPP_HARNESS_H
#include <cstddef>
#include <cstdint>
struct parsarium_mp4_result { char title[128]; std::int64_t duration_ms; };
bool parsarium_parse_mp4(const std::uint8_t *data, std::size_t size,
                         parsarium_mp4_result *result);
#endif
