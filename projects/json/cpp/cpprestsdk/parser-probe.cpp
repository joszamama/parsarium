#include <cpprest/json.h>
#include <exception>
#include <fstream>
#include <iterator>
#include <string>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    const std::string input(std::istreambuf_iterator<char>{file}, {});
    if (input.empty() || input.size() > (1u << 20)) return 2;
    web::json::keep_object_element_order(true);
    try { (void)web::json::value::parse(input); }
    catch (const std::exception&) { return 1; }
    return 0;
}
