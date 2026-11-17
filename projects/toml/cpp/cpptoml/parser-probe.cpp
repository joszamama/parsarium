// Parser-only probe for AFL++ feedback: cpptoml::parser(std::istream&).parse() and nothing else
// (no tree walk or output formatting).
#include <limits>  // cpptoml.h needs std::numeric_limits but does not include <limits>

#include <cpptoml.h>

#include <fstream>
#include <iterator>
#include <sstream>
#include <string>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    const std::string input(std::istreambuf_iterator<char>{file}, {});
    if (input.empty() || input.size() > (1u << 20)) return 2;
    std::istringstream stream(input);
    try { (void)cpptoml::parser(stream).parse(); }
    catch (const cpptoml::parse_exception &) { return 1; }
    return 0;
}
