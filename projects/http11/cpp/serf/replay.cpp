#include "harness.h"

#include <cstdio>
#include <string>
#include <vector>

static std::string json_string(const std::string &value) {
    std::string out = "\"";
    for (unsigned char c : value) {
        if (c == '"' || c == '\\') {
            out += '\\';
            out += static_cast<char>(c);
        } else if (c < 0x20 || c >= 0x7f) {
            char escaped[7];
            std::snprintf(escaped, sizeof(escaped), "\\u%04x", c);
            out += escaped;
        } else {
            out += static_cast<char>(c);
        }
    }
    return out + "\"";
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    std::vector<std::uint8_t> input;
    std::uint8_t buffer[4096];
    for (;;) {
        std::size_t count = std::fread(buffer, 1, sizeof(buffer), file);
        input.insert(input.end(), buffer, buffer + count);
        if (input.size() > (1u << 20)) {
            std::fclose(file);
            return 4;
        }
        if (count < sizeof(buffer)) {
            if (std::ferror(file)) {
                std::fclose(file);
                return 4;
            }
            break;
        }
    }
    std::fclose(file);
    ParsariumHttpResponse result{};
    if (!parsarium_parse_http_response(input.data(), input.size(), &result)) {
        std::fprintf(stderr, "%s\n",
                     result.error.empty() ? "Serf response parse failed" : result.error.c_str());
        return 5;
    }
    std::printf("{\"version\":\"%d.%d\",\"status\":%d,\"reason\":%s,\"content_type\":%s,"
                "\"body\":%s}\n",
                result.major, result.minor, result.status, json_string(result.reason).c_str(),
                result.has_content_type ? json_string(result.content_type).c_str() : "null",
                json_string(result.body).c_str());
    return 0;
}
