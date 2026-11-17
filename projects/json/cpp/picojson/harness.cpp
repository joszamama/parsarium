#include <picojson.h>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <iterator>
#include <string>

#ifdef PARSARIUM_FUZZER
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (!data || size == 0 || size > (1u << 20)) return 0;
    picojson::value document;
    std::string error;
    const char *begin = reinterpret_cast<const char *>(data);
    (void)picojson::parse(document, begin, begin + size, &error);
    return 0;
}
#else
// The printer is harness code; it does not call the picojson serializer.
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

static void print(const picojson::value &value) {
    if (value.is<picojson::null>()) {
        std::cout << "null";
    } else if (value.is<bool>()) {
        std::cout << (value.get<bool>() ? "true" : "false");
    } else if (value.is<int64_t>()) {
        std::cout << value.get<int64_t>();
    } else if (value.is<double>()) {
        char buf[64];
        std::snprintf(buf, sizeof buf, "%.17g", value.get<double>());
        std::string text(buf);
        if (text.find_first_of(".eEn") == std::string::npos) text += ".0";
        std::cout << text;
    } else if (value.is<std::string>()) {
        print_string(value.get<std::string>());
    } else if (value.is<picojson::array>()) {
        std::cout << '[';
        bool first = true;
        for (const auto &item : value.get<picojson::array>()) {
            if (!first) std::cout << ',';
            first = false;
            print(item);
        }
        std::cout << ']';
    } else {
        // picojson::object is std::map: members come back in sorted key order.
        std::cout << '{';
        bool first = true;
        for (const auto &member : value.get<picojson::object>()) {
            if (!first) std::cout << ',';
            first = false;
            print_string(member.first);
            std::cout << ':';
            print(member.second);
        }
        std::cout << '}';
    }
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    std::string input(std::istreambuf_iterator<char>{file}, {});
    if (input.empty() || input.size() > (1u << 20)) return 2;
    picojson::value document;
    const std::string error = picojson::parse(document, input);
    if (!error.empty()) {
        std::cerr << error << '\n';
        return 1;
    }
    print(document);
    std::cout << '\n';
    return 0;
}
#endif
