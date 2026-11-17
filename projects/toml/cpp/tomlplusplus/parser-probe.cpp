// Parser-only probe for AFL++ feedback: toml::parse(std::string_view) and nothing else
// (no tree walk or output formatting).
#include <toml++/toml.hpp>

#include <fstream>
#include <iterator>
#include <string>
#include <string_view>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    const std::string input(std::istreambuf_iterator<char>{file}, {});
    if (input.empty() || input.size() > (1u << 20)) return 2;
    try { (void)toml::parse(std::string_view(input)); }
    catch (const toml::parse_error &) { return 1; }
    return 0;
}
