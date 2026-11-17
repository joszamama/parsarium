#include <simdjson.h>

#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>

static bool parse_json(const uint8_t *data, size_t size, bool print_tree) {
    if (!data || size == 0 || size > (1u << 20)) return false;
    // The documented pointer+length overload copies into a padded buffer.
    simdjson::dom::parser parser;
    simdjson::dom::element root;
    auto error = parser.parse(reinterpret_cast<const char *>(data), size).get(root);
    if (error) return false;
    if (print_tree) std::cout << root << '\n';
    return true;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    (void)parse_json(data, size, false);
    return 0;
}

#ifndef PARSARIUM_FUZZER
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    auto *data = static_cast<uint8_t *>(std::malloc((1u << 20) + 1));
    if (!data) { std::fclose(file); return 4; }
    size_t size = std::fread(data, 1, 1u << 20, file);
    if (std::ferror(file) || (size == (1u << 20) && std::fgetc(file) != EOF)) {
        std::free(data); std::fclose(file); return 4;
    }
    std::fclose(file);
    bool parsed = parse_json(data, size, true);
    std::free(data);
    return parsed ? 0 : 5;
}
#endif
