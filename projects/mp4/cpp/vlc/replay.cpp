#include "harness.h"
#include <cstdio>
#include <string>

namespace {

std::string json_string(const std::string &text) {
    std::string out = "\"";
    for (unsigned char c : text) {
        if (c == '"' || c == '\\') { out += '\\'; out += static_cast<char>(c); }
        else if (c < 32) { char escaped[7]; std::snprintf(escaped, sizeof(escaped), "\\u%04x", c); out += escaped; }
        else out += static_cast<char>(c);
    }
    return out + '"';
}

}  // namespace

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    static std::uint8_t data[1u << 20];
    std::size_t size = std::fread(data, 1, sizeof(data), file);
    if (std::ferror(file) || (size == sizeof(data) && std::fgetc(file) != EOF)) { std::fclose(file); return 4; }
    std::fclose(file);
    parsarium_mp4_result result;
    if (!parsarium_parse_mp4(data, size, result)) return 5;
    std::printf("{\"title\":%s,\"video_tracks\":%u,\"audio_tracks\":%u,\"duration_ms\":%lld,"
                "\"video_codec\":%s,\"audio_codec\":%s,\"width\":%u,\"height\":%u}\n",
                json_string(result.title).c_str(), result.video_tracks, result.audio_tracks,
                result.duration_ms, json_string(result.video_codec).c_str(),
                json_string(result.audio_codec).c_str(), result.width, result.height);
    return 0;
}
