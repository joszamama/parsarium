#include <rapidxml.hpp>
#include <fstream>
#include <iterator>
#include <string>
#include <vector>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    const std::string input(std::istreambuf_iterator<char>{file}, {});
    if (input.empty() || input.size() > (1u << 20) ||
        input.find('\0') != std::string::npos) return 2;
    std::vector<char> bytes(input.begin(), input.end());
    bytes.push_back('\0');
    rapidxml::xml_document<> document;
    try { document.parse<0>(bytes.data()); }
    catch (const rapidxml::parse_error &) { return 1; }
    return document.first_node() ? 0 : 1;
}
