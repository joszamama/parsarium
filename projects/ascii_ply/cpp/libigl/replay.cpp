#include "harness.h"

#include <cstdio>
#include <vector>

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
    ParsariumPlyResult result{};
    // igl::readPLY prints its own reason to stderr when it returns false.
    if (!parsarium_parse_ply(input.data(), input.size(), &result)) return 5;
    std::printf("{\"vertices\":%zu,\"faces\":%zu,\"face\":[", result.vertices, result.faces);
    for (std::size_t i = 0; i < result.face.size(); ++i)
        std::printf(i ? ",%d" : "%d", result.face[i]);
    std::printf("]}\n");
    return 0;
}
