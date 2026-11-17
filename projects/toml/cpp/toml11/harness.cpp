// toml11 4.4.0: documented toml::parse_str(std::string, toml::spec::v(1, 0, 0)) -> toml::value,
// then a walk over toml::value (value_t, as_table/as_array/as_*) that prints the protocol's typed tree.
#include <toml.hpp>

#include "typed-tree.h"

#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iterator>
#include <string>

static uint32_t nanoseconds(const toml::local_time &t) {
    return static_cast<uint32_t>(t.millisecond) * 1000000u + static_cast<uint32_t>(t.microsecond) * 1000u +
           static_cast<uint32_t>(t.nanosecond);
}

static std::string date_text(const toml::local_date &d) {
    return parsarium::date_text(d.year, static_cast<unsigned>(d.month) + 1u, d.day);  // month is [0, 11]
}

static std::string time_text(const toml::local_time &t) {
    return parsarium::time_text(t.hour, t.minute, t.second, nanoseconds(t));
}

static void walk(const toml::value &value, std::string &out) {
    using parsarium::scalar;
    switch (value.type()) {
    case toml::value_t::table: {
        out += '{';
        bool first = true;
        for (const auto &item : value.as_table()) {
            if (!first) out += ',';
            first = false;
            parsarium::json_string(out, item.first);
            out += ':';
            walk(item.second, out);
        }
        out += '}';
        break;
    }
    case toml::value_t::array: {
        out += '[';
        bool first = true;
        for (const auto &child : value.as_array()) {
            if (!first) out += ',';
            first = false;
            walk(child, out);
        }
        out += ']';
        break;
    }
    case toml::value_t::string:
        scalar(out, "string", value.as_string());
        break;
    case toml::value_t::integer:
        scalar(out, "integer", std::to_string(value.as_integer()));
        break;
    case toml::value_t::floating:
        scalar(out, "float", parsarium::float_text(value.as_floating()));
        break;
    case toml::value_t::boolean:
        scalar(out, "bool", value.as_boolean() ? "true" : "false");
        break;
    case toml::value_t::local_date:
        scalar(out, "date-local", date_text(value.as_local_date()));
        break;
    case toml::value_t::local_time:
        scalar(out, "time-local", time_text(value.as_local_time()));
        break;
    case toml::value_t::local_datetime: {
        const toml::local_datetime &dt = value.as_local_datetime();
        scalar(out, "datetime-local", date_text(dt.date) + "T" + time_text(dt.time));
        break;
    }
    case toml::value_t::offset_datetime: {
        const toml::offset_datetime &dt = value.as_offset_datetime();
        const int offset = static_cast<int>(dt.offset.hour) * 60 + static_cast<int>(dt.offset.minute);
        scalar(out, "datetime", parsarium::utc_instant(dt.date.year, static_cast<unsigned>(dt.date.month) + 1u,
                                                       dt.date.day, dt.time.hour, dt.time.minute,
                                                       dt.time.second, nanoseconds(dt.time), offset));
        break;
    }
    default:
        out += "\"unsupported value\"";
    }
}

#ifdef PARSARIUM_FUZZER
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size > (1u << 20)) return 0;
    try {
        toml::value root = toml::parse_str(std::string(reinterpret_cast<const char *>(data), size),
                                           toml::spec::v(1, 0, 0));
        std::string out;
        walk(root, out);
    } catch (const toml::exception &) {
    }
    return 0;
}
#else
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 3;
    std::string input(std::istreambuf_iterator<char>{file}, {});
    if (input.empty() || input.size() > (1u << 20)) return 4;
    try {
        toml::value root = toml::parse_str(std::move(input), toml::spec::v(1, 0, 0));
        std::string out;
        walk(root, out);
        std::puts(out.c_str());
    } catch (const toml::exception &error) {
        std::fprintf(stderr, "toml::exception: %s\n", error.what());
        return 5;
    }
    return 0;
}
#endif
