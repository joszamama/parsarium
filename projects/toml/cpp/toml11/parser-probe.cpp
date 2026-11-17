// Parser-only probe for AFL++ feedback: toml::parse_str(std::string, spec v1.0.0) and nothing else
// (no tree walk or output formatting).
#include <toml.hpp>

#include <fstream>
#include <iterator>
#include <string>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    std::string input(std::istreambuf_iterator<char>{file}, {});
    if (input.empty() || input.size() > (1u << 20)) return 2;
    try { (void)toml::parse_str(std::move(input), toml::spec::v(1, 0, 0)); }
    catch (const toml::exception &) { return 1; }
    return 0;
}
