#include <jsoncons/json.hpp>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <iterator>
#include <string>

#ifdef PARSARIUM_FUZZER
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (!data || size == 0 || size > (1u << 20)) return 0;
    try { (void)jsoncons::ojson::parse(reinterpret_cast<const char*>(data), size); }
    catch (const std::exception&) {}
    return 0;
}
#else
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    std::string input(std::istreambuf_iterator<char>{file}, {});
    if (input.empty() || input.size() > (1u << 20)) return 2;
    try {
        auto document = jsoncons::ojson::parse(input.data(), input.size());
        document.dump(std::cout);
        std::cout << '\n';
    } catch (const std::exception &ex) {
        std::cerr << ex.what() << '\n';
        return 1;
    }
    return 0;
}
#endif
