#include "harness.h"
#include <cstdio>
#include <string>

// Replay only records coverage and output. libass and fontconfig keep
// process-lifetime allocations, so leak reports at exit are not parser
// results here; the fuzzer keeps the sanitizer defaults.
extern "C" const char *__asan_default_options() { return "detect_leaks=0"; }

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
    parsarium_mp3_result result;
    if (!parsarium_parse_mp3(data, size, result)) return 5;
    std::printf("{\"title\":%s,\"codec\":%s,\"duration_ms\":%lld}\n",
                json_string(result.title).c_str(), json_string(result.codec).c_str(),
                static_cast<long long>(result.duration_ms));
    return 0;
}
