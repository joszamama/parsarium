#ifndef PARSARIUM_VLC_MP4_HARNESS_H
#define PARSARIUM_VLC_MP4_HARNESS_H
#include <cstddef>
#include <cstdint>
#include <string>

struct parsarium_mp4_result {
    std::string title, video_codec, audio_codec;
    unsigned video_tracks = 0, audio_tracks = 0, width = 0, height = 0;
    long long duration_ms = 0;
};

// Parses one MP4 through libVLC's local-path media API. Returns false unless
// libVLC finished parsing and exposed at least one track.
bool parsarium_parse_mp4(const std::uint8_t *data, std::size_t size, parsarium_mp4_result &result);
#endif
