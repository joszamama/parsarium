#include "harness.h"
#include <cstdio>
#include <cstdlib>
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    auto *data = static_cast<std::uint8_t *>(std::malloc(1u << 20));
    if (!data) { std::fclose(file); return 4; }
    std::size_t size = std::fread(data, 1, 1u << 20, file);
    if (std::ferror(file) || (size == (1u << 20) && std::fgetc(file) != EOF)) { std::free(data); std::fclose(file); return 4; }
    std::fclose(file);
    Result result{};
    bool ok = parse_data(data, size, &result);
    std::free(data);
    if (!ok) return 5;
    std::printf("{\"pages\":%d}\n", result.pages);
    return 0;
}
