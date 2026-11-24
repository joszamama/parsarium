#include "harness.h"
#include <cstdio>
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    static std::uint8_t data[1u << 20];
    std::size_t size = std::fread(data, 1, sizeof(data), file);
    if (std::ferror(file) || (size == sizeof(data) && std::fgetc(file) != EOF)) { std::fclose(file); return 4; }
    std::fclose(file);
    Result result{};
    if (!parse_data(data, size, &result)) {
        std::fprintf(stderr, "%s\n", result.error.c_str());
        return 5;
    }
    // Width, height and frame count are whole numbers. CAP_PROP_FPS is printed with
    // %.17g so a fractional rate is not rounded; an integral rate prints as before.
    std::printf("{\"width\":%.0f,\"height\":%.0f,\"frames\":%.0f,\"fps\":%.17g}\n",
                result.width, result.height, result.frames, result.fps);
    return 0;
}
