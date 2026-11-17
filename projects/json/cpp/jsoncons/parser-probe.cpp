#include <jsoncons/json.hpp>
#include <fstream>
#include <iterator>
#include <string>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    const std::string input(std::istreambuf_iterator<char>{file}, {});
    if (input.empty() || input.size() > (1u << 20)) return 2;
    try { (void)jsoncons::ojson::parse(input.data(), input.size()); }
    catch (const std::exception&) { return 1; }
    return 0;
}
