#include <tao/json.hpp>
#include <cstdint>
#include <cstdio>
#include <exception>
#include <fstream>
#include <iostream>
#include <iterator>
#include <string>

#ifdef PARSARIUM_FUZZER
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (!data || size == 0 || size > (1u << 20)) return 0;
    try { (void)tao::json::from_string(reinterpret_cast<const char *>(data), size, "input"); }
    catch (const std::exception&) {}
    return 0;
}
#else
// The printer is harness code; it does not call the taoJSON serializer.
static void print_string(std::string_view text) {
    std::cout << '"';
    for (unsigned char ch : text) {
        if (ch == '"' || ch == '\\') {
            std::cout << '\\' << static_cast<char>(ch);
        } else if (ch < 0x20) {
            char buf[8];
            std::snprintf(buf, sizeof buf, "\\u%04x", ch);
            std::cout << buf;
        } else {
            std::cout << static_cast<char>(ch);
        }
    }
    std::cout << '"';
}

static void print(const tao::json::value &value) {
    switch (value.type()) {
    case tao::json::type::NULL_: std::cout << "null"; return;
    case tao::json::type::BOOLEAN: std::cout << (value.get_boolean() ? "true" : "false"); return;
    case tao::json::type::SIGNED: std::cout << value.get_signed(); return;
    case tao::json::type::UNSIGNED: std::cout << value.get_unsigned(); return;
    case tao::json::type::DOUBLE: {
        char buf[64];
        std::snprintf(buf, sizeof buf, "%.17g", value.get_double());
        std::string text(buf);
        if (text.find_first_of(".eEn") == std::string::npos) text += ".0";
        std::cout << text;
        return;
    }
    case tao::json::type::STRING: print_string(value.get_string()); return;
    case tao::json::type::ARRAY: {
        std::cout << '[';
        bool first = true;
        for (const auto &item : value.get_array()) {
            if (!first) std::cout << ',';
            first = false;
            print(item);
        }
        std::cout << ']';
        return;
    }
    case tao::json::type::OBJECT: {
        // tao::json::value objects are std::map: members come back in sorted key order.
        std::cout << '{';
        bool first = true;
        for (const auto &member : value.get_object()) {
            if (!first) std::cout << ',';
            first = false;
            print_string(member.first);
            std::cout << ':';
            print(member.second);
        }
        std::cout << '}';
        return;
    }
    default:
        throw std::runtime_error("unexpected taoJSON value type");
    }
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    std::string input(std::istreambuf_iterator<char>{file}, {});
    if (input.empty() || input.size() > (1u << 20)) return 2;
    try {
        const tao::json::value document = tao::json::from_string(input.data(), input.size(), "input");
        print(document);
        std::cout << '\n';
    } catch (const std::exception &ex) {
        std::cerr << ex.what() << '\n';
        return 1;
    }
    return 0;
}
#endif
