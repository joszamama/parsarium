#include "harness.h"

#include <fstream>
#include <iostream>
#include <iterator>
#include <vector>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 3;
    constexpr std::size_t limit = 8u << 20;
    std::vector<std::uint8_t> data;
    data.reserve(limit);
    std::istreambuf_iterator<char> it(file), end;
    for (; it != end && data.size() <= limit; ++it) data.push_back(static_cast<std::uint8_t>(*it));
    if (file.bad() || data.size() > limit) return 4;
    Result result;
    if (!parse_data(data.data(), data.size(), result)) return 5;
    std::cout << "{\"pages\":" << result.pages << "}\n";
    return 0;
}
