#ifndef PARSARIUM_MPV_MP4_HARNESS_H
#define PARSARIUM_MPV_MP4_HARNESS_H
#include <cstddef>
#include <cstdint>
#include <string>

struct parsarium_mp4_result {
    std::string container, title, video_codec, audio_codec;
};

// Loads one MP4 through libmpv's loadfile command on a local path. Returns false
// unless libmpv reported FILE_LOADED with a container and a video and audio track.
bool parsarium_parse_mp4(const std::uint8_t *data, std::size_t size, parsarium_mp4_result &result);
#endif
