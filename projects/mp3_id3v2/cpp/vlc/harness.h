#ifndef PARSARIUM_VLC_MP3_HARNESS_H
#define PARSARIUM_VLC_MP3_HARNESS_H
#include <cstddef>
#include <cstdint>
#include <string>

struct parsarium_mp3_result {
    std::string title, audio_codec;
    unsigned audio_tracks = 0, mp3_tracks = 0, rate = 0, channels = 0;
};

// Parses one tagged MP3 through libVLC's local-path media API. Returns false
// unless libVLC finished parsing and exposed at least one track.
bool parsarium_parse_mp3(const std::uint8_t *data, std::size_t size, parsarium_mp3_result &result);
#endif
