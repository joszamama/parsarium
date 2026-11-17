#include <boost/json/src.hpp>

#include <cmath>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>

namespace json = boost::json;

static void print_string(json::string_view text) {
    std::putchar('"');
    for (unsigned char c : text) {
        if (c == '"' || c == '\\') {
            std::putchar('\\');
            std::putchar(c);
        } else if (c < 0x20) {
            std::printf("\\u%04x", c);
        } else {
            std::putchar(c);  // UTF-8 bytes pass through unchanged
        }
    }
    std::putchar('"');
}

// Prints the parsed DOM in insertion order. Integers stay integers and doubles
// always carry a fraction or exponent, so the checker can compare kinds.
static void print_value(const json::value &value) {
    switch (value.kind()) {
    case json::kind::object: {
        std::putchar('{');
        bool first = true;
        for (const auto &member : value.get_object()) {
            if (!first) std::putchar(',');
            first = false;
            print_string(member.key());
            std::putchar(':');
            print_value(member.value());
        }
        std::putchar('}');
        break;
    }
    case json::kind::array: {
        std::putchar('[');
        bool first = true;
        for (const auto &item : value.get_array()) {
            if (!first) std::putchar(',');
            first = false;
            print_value(item);
        }
        std::putchar(']');
        break;
    }
    case json::kind::string: print_string(value.get_string()); break;
    case json::kind::int64: std::printf("%lld", (long long)value.get_int64()); break;
    case json::kind::uint64: std::printf("%llu", (unsigned long long)value.get_uint64()); break;
    case json::kind::double_: {
        char text[40];
        std::snprintf(text, sizeof(text), "%.17g", value.get_double());
        if (!std::isfinite(value.get_double())) std::strcpy(text, "null");
        else if (!std::strpbrk(text, ".e")) std::strcat(text, ".0");
        std::fputs(text, stdout);
        break;
    }
    case json::kind::bool_: std::fputs(value.get_bool() ? "true" : "false", stdout); break;
    case json::kind::null: std::fputs("null", stdout); break;
    }
}

static bool parse_json(const uint8_t *data, size_t size, bool print_tree) {
    if (!data || size == 0 || size > (1u << 20)) return false;
    // Documented boost::json::parse(string_view, error_code&); default options are strict.
    boost::system::error_code error;
    json::value root = json::parse(
        json::string_view(reinterpret_cast<const char *>(data), size), error);
    if (error) return false;
    if (!root.is_object() && !root.is_array()) return false;  // controls cover object/array roots
    if (print_tree) {
        print_value(root);
        std::putchar('\n');
    }
    return true;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    (void)parse_json(data, size, false);
    return 0;
}

#ifndef PARSARIUM_FUZZER
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    auto *data = static_cast<uint8_t *>(std::malloc((1u << 20) + 1));
    if (!data) { std::fclose(file); return 4; }
    size_t size = std::fread(data, 1, 1u << 20, file);
    if (std::ferror(file) || (size == (1u << 20) && std::fgetc(file) != EOF)) {
        std::free(data); std::fclose(file); return 4;
    }
    std::fclose(file);
    bool parsed = parse_json(data, size, true);
    std::free(data);
    return parsed ? 0 : 5;
}
#endif
