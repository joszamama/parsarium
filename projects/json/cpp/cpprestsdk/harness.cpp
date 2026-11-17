#include <cpprest/json.h>
#include <cstdint>
#include <cstdio>
#include <exception>
#include <fstream>
#include <iostream>
#include <iterator>
#include <stdexcept>
#include <string>

#ifdef PARSARIUM_FUZZER
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (!data || size == 0 || size > (1u << 20)) return 0;
    web::json::keep_object_element_order(true);
    try { (void)web::json::value::parse(std::string(reinterpret_cast<const char *>(data), size)); }
    catch (const std::exception&) {}
    return 0;
}
#else
// The printer is harness code; it does not call the cpprest serializer.
static void print_string(const std::string &text) {
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

static void print(const web::json::value &value) {
    switch (value.type()) {
    case web::json::value::Null: std::cout << "null"; return;
    case web::json::value::Boolean: std::cout << (value.as_bool() ? "true" : "false"); return;
    case web::json::value::Number: {
        const web::json::number &number = value.as_number();
        if (number.is_int64()) { std::cout << number.to_int64(); return; }
        if (number.is_uint64()) { std::cout << number.to_uint64(); return; }
        if (number.is_integral()) throw std::runtime_error("integral number outside 64-bit range");
        char buf[64];
        std::snprintf(buf, sizeof buf, "%.17g", value.as_double());
        std::string text(buf);
        if (text.find_first_of(".eEn") == std::string::npos) text += ".0";
        std::cout << text;
        return;
    }
    case web::json::value::String: print_string(value.as_string()); return;
    case web::json::value::Array: {
        std::cout << '[';
        bool first = true;
        for (const auto &item : value.as_array()) {
            if (!first) std::cout << ',';
            first = false;
            print(item);
        }
        std::cout << ']';
        return;
    }
    case web::json::value::Object: {
        // keep_object_element_order(true) keeps members in source order.
        std::cout << '{';
        bool first = true;
        for (const auto &member : value.as_object()) {
            if (!first) std::cout << ',';
            first = false;
            print_string(member.first);
            std::cout << ':';
            print(member.second);
        }
        std::cout << '}';
        return;
    }
    }
    throw std::runtime_error("unexpected cpprest JSON value type");
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    std::string input(std::istreambuf_iterator<char>{file}, {});
    if (input.empty() || input.size() > (1u << 20)) return 2;
    // Documented global switch: without it, parsed objects are sorted by key.
    web::json::keep_object_element_order(true);
    try {
        const web::json::value document = web::json::value::parse(input);
        print(document);
        std::cout << '\n';
    } catch (const std::exception &ex) {
        std::cerr << ex.what() << '\n';
        return 1;
    }
    return 0;
}
#endif
