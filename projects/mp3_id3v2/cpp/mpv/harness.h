#ifndef PARSARIUM_MPV_MP3_HARNESS_H
#define PARSARIUM_MPV_MP3_HARNESS_H
#include <cstddef>
#include <cstdint>
#include <string>

struct parsarium_mp3_result {
    std::string title, codec;
    std::int64_t duration_ms = 0;
};

// Loads one tagged MP3 through libmpv's loadfile command on a local path. Returns
// false unless libmpv reported FILE_LOADED with an audio first track, its codec
// and a finite positive duration.
bool parsarium_parse_mp3(const std::uint8_t *data, std::size_t size, parsarium_mp3_result &result);
#endif
