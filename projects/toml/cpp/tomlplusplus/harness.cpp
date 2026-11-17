// toml++ 3.4.0: documented toml::parse(std::string_view) -> toml::table, then a
// walk over toml::node (table, array, value<T>) that prints the protocol's typed tree.
#include <toml++/toml.hpp>

#include "typed-tree.h"

#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iterator>
#include <string>
#include <string_view>

static void walk(const toml::node &node, std::string &out) {
    using parsarium::scalar;
    switch (node.type()) {
    case toml::node_type::table: {
        out += '{';
        bool first = true;
        for (auto &&[key, child] : *node.as_table()) {
            if (!first) out += ',';
            first = false;
            parsarium::json_string(out, std::string(key.str()));
            out += ':';
            walk(child, out);
        }
        out += '}';
        break;
    }
    case toml::node_type::array: {
        out += '[';
        bool first = true;
        for (const toml::node &child : *node.as_array()) {
            if (!first) out += ',';
            first = false;
            walk(child, out);
        }
        out += ']';
        break;
    }
    case toml::node_type::string:
        scalar(out, "string", node.as_string()->get());
        break;
    case toml::node_type::integer:
        scalar(out, "integer", std::to_string(node.as_integer()->get()));
        break;
    case toml::node_type::floating_point:
        scalar(out, "float", parsarium::float_text(node.as_floating_point()->get()));
        break;
    case toml::node_type::boolean:
        scalar(out, "bool", node.as_boolean()->get() ? "true" : "false");
        break;
    case toml::node_type::date: {
        const toml::date &d = node.as_date()->get();
        scalar(out, "date-local", parsarium::date_text(d.year, d.month, d.day));
        break;
    }
    case toml::node_type::time: {
        const toml::time &t = node.as_time()->get();
        scalar(out, "time-local", parsarium::time_text(t.hour, t.minute, t.second, t.nanosecond));
        break;
    }
    case toml::node_type::date_time: {
        const toml::date_time &dt = node.as_date_time()->get();
        const toml::date &d = dt.date;
        const toml::time &t = dt.time;
        if (dt.offset)
            scalar(out, "datetime", parsarium::utc_instant(d.year, d.month, d.day, t.hour, t.minute,
                                                           t.second, t.nanosecond, dt.offset->minutes));
        else
            scalar(out, "datetime-local", parsarium::date_text(d.year, d.month, d.day) + "T" +
                                              parsarium::time_text(t.hour, t.minute, t.second, t.nanosecond));
        break;
    }
    default:
        out += "\"unsupported node\"";
    }
}

#ifdef PARSARIUM_FUZZER
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size > (1u << 20)) return 0;
    try {
        toml::table root = toml::parse(std::string_view(reinterpret_cast<const char *>(data), size));
        std::string out;
        walk(root, out);
    } catch (const toml::parse_error &) {
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
    try {
        toml::table root = toml::parse(std::string_view(input));
        std::string out;
        walk(root, out);
        std::puts(out.c_str());
    } catch (const toml::parse_error &error) {
        std::fprintf(stderr, "toml::parse_error: %s\n", std::string(error.description()).c_str());
        return 5;
    }
    return 0;
}
#endif
