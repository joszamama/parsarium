// cpptoml 0.1.1: documented cpptoml::parser(std::istream&).parse() -> std::shared_ptr<cpptoml::table>,
// then a walk over cpptoml::base (table, array, table_array, value<T>) that prints the protocol's typed tree.
// cpptoml.h uses std::numeric_limits without including <limits>; current libstdc++
// no longer pulls it in transitively, so it is included first (no source patch).
#include <limits>

#include <cpptoml.h>

#include "typed-tree.h"

#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iterator>
#include <sstream>
#include <string>

static std::string date_text(const cpptoml::local_date &d) {
    return parsarium::date_text(d.year, static_cast<unsigned>(d.month), static_cast<unsigned>(d.day));
}

static std::string time_text(const cpptoml::local_time &t) {
    return parsarium::time_text(static_cast<unsigned>(t.hour), static_cast<unsigned>(t.minute),
                                static_cast<unsigned>(t.second), static_cast<uint32_t>(t.microsecond) * 1000u);
}

static void walk(const std::shared_ptr<cpptoml::base> &node, std::string &out) {
    using parsarium::scalar;
    if (node->is_table()) {
        out += '{';
        bool first = true;
        for (const auto &item : *node->as_table()) {
            if (!first) out += ',';
            first = false;
            parsarium::json_string(out, item.first);
            out += ':';
            walk(item.second, out);
        }
        out += '}';
    } else if (node->is_table_array()) {
        out += '[';
        bool first = true;
        for (const auto &child : node->as_table_array()->get()) {
            if (!first) out += ',';
            first = false;
            walk(child, out);
        }
        out += ']';
    } else if (node->is_array()) {
        out += '[';
        bool first = true;
        for (const auto &child : node->as_array()->get()) {
            if (!first) out += ',';
            first = false;
            walk(child, out);
        }
        out += ']';
    } else if (auto v = node->as<std::string>()) {
        scalar(out, "string", v->get());
    } else if (auto v = node->as<int64_t>()) {
        scalar(out, "integer", std::to_string(v->get()));
    } else if (auto v = node->as<double>()) {
        scalar(out, "float", parsarium::float_text(v->get()));
    } else if (auto v = node->as<bool>()) {
        scalar(out, "bool", v->get() ? "true" : "false");
    } else if (auto v = node->as<cpptoml::offset_datetime>()) {
        const cpptoml::offset_datetime &dt = v->get();
        const int offset = dt.hour_offset * 60 + dt.minute_offset;
        scalar(out, "datetime", parsarium::utc_instant(dt.year, static_cast<unsigned>(dt.month),
                                                       static_cast<unsigned>(dt.day), static_cast<unsigned>(dt.hour),
                                                       static_cast<unsigned>(dt.minute), static_cast<unsigned>(dt.second),
                                                       static_cast<uint32_t>(dt.microsecond) * 1000u, offset));
    } else if (auto v = node->as<cpptoml::local_datetime>()) {
        const cpptoml::local_datetime &dt = v->get();
        scalar(out, "datetime-local", date_text(dt) + "T" + time_text(dt));
    } else if (auto v = node->as<cpptoml::local_date>()) {
        scalar(out, "date-local", date_text(v->get()));
    } else if (auto v = node->as<cpptoml::local_time>()) {
        scalar(out, "time-local", time_text(v->get()));
    } else {
        out += "\"unsupported value\"";
    }
}

#ifdef PARSARIUM_FUZZER
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size > (1u << 20)) return 0;
    std::istringstream stream(std::string(reinterpret_cast<const char *>(data), size));
    try {
        std::shared_ptr<cpptoml::table> root = cpptoml::parser(stream).parse();
        std::string out;
        walk(root, out);
    } catch (const cpptoml::parse_exception &) {
    }
    return 0;
}
#else
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 3;
    const std::string input(std::istreambuf_iterator<char>{file}, {});
    if (input.empty() || input.size() > (1u << 20)) return 4;
    std::istringstream stream(input);
    try {
        std::shared_ptr<cpptoml::table> root = cpptoml::parser(stream).parse();
        std::string out;
        walk(root, out);
        std::puts(out.c_str());
    } catch (const cpptoml::parse_exception &error) {
        std::fprintf(stderr, "cpptoml::parse_exception: %s\n", error.what());
        return 5;
    }
    return 0;
}
#endif
