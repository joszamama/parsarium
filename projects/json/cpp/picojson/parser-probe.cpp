#include <picojson.h>
#include <fstream>
#include <iterator>
#include <string>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    const std::string input(std::istreambuf_iterator<char>{file}, {});
    if (input.empty() || input.size() > (1u << 20)) return 2;
    picojson::value document;
    const std::string error = picojson::parse(document, input);
    return error.empty() ? 0 : 1;
}
