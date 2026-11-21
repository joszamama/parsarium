#include <glaze/json/generic.hpp>

#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>

static bool parse_json(const uint8_t* data, size_t size, bool print_tree) {
    if (!data || size == 0 || size > (1u << 20)) return false;
    // The documented generic_i64 reader accepts a local string buffer and
    // keeps object insertion order while preserving signed integer kinds.
    std::string buffer(reinterpret_cast<const char*>(data), size);
    glz::generic_i64 root{};
    if (glz::read_json(root, buffer)) return false;
    if (print_tree) {
        auto output = root.dump();
        if (!output) return false;
        // glaze's compact writer emits no whitespace, so a byte below 0x20 can
        // only be inside a string; write it as a \u00XX escape so the printed
        // tree is RFC 8259 text the checker can read.
        for (unsigned char c : *output) {
            if (c < 0x20) std::printf("\\u%04x", c);
            else std::putchar(c);
        }
        std::putchar('\n');
    }
    return true;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
    (void)parse_json(data, size, false);
    return 0;
}

#ifndef PARSARIUM_FUZZER
int main(int argc, char** argv) {
    if (argc != 2) return 2;
    FILE* file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    auto* data = static_cast<uint8_t*>(std::malloc((1u << 20) + 1));
    if (!data) { std::fclose(file); return 4; }
    const size_t size = std::fread(data, 1, 1u << 20, file);
    if (std::ferror(file) || (size == (1u << 20) && std::fgetc(file) != EOF)) {
        std::free(data); std::fclose(file); return 4;
    }
    std::fclose(file);
    const bool parsed = parse_json(data, size, true);
    std::free(data);
    return parsed ? 0 : 5;
}
#endif
