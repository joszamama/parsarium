#include <glaze/json/generic.hpp>

#include <fstream>
#include <iterator>
#include <string>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    const std::string buffer(std::istreambuf_iterator<char>{file}, {});
    if (buffer.empty() || buffer.size() > (1u << 20)) return 2;
    glz::generic_i64 root{};
    if (glz::read_json(root, buffer)) return 1;
    return root.is_object() || root.is_array() ? 0 : 1;
}
