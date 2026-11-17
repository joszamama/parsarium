// Typed-tree output helpers for the TOML cell protocol (catalog/toml/PROTOCOL.md).
// The harness passes values taken from the library's own node API; nothing here
// reads or re-parses TOML text.
#ifndef PARSARIUM_TOML_TYPED_TREE_H
#define PARSARIUM_TOML_TYPED_TREE_H

#include <charconv>
#include <cstdint>
#include <cstdio>
#include <string>
#include <system_error>

namespace parsarium {

inline void json_string(std::string &out, const std::string &text) {
    out += '"';
    for (unsigned char c : text) {
        switch (c) {
        case '"': out += "\\\""; break;
        case '\\': out += "\\\\"; break;
        case '\n': out += "\\n"; break;
        case '\t': out += "\\t"; break;
        case '\r': out += "\\r"; break;
        default:
            if (c < 0x20) {
                char buffer[8];
                std::snprintf(buffer, sizeof buffer, "\\u%04x", c);
                out += buffer;
            } else {
                out += static_cast<char>(c);  // UTF-8 bytes pass through unchanged
            }
        }
    }
    out += '"';
}

inline void scalar(std::string &out, const char *type, const std::string &value) {
    out += "{\"type\":\"";
    out += type;
    out += "\",\"value\":";
    json_string(out, value);
    out += '}';
}

// Shortest round-trip digits (std::to_chars), written positionally with at
// least one fractional digit: 1e3 -> 1000.0, 1.5625e-2 -> 0.015625.
inline std::string float_text(double value) {
    char buffer[64];
    auto result = std::to_chars(buffer, buffer + sizeof buffer, value, std::chars_format::scientific);
    if (result.ec != std::errc()) return "error";
    std::string text(buffer, result.ptr);
    bool negative = !text.empty() && text[0] == '-';
    if (negative) text.erase(0, 1);
    std::size_t e = text.find('e');
    std::string mantissa = text.substr(0, e);
    int exponent = std::stoi(text.substr(e + 1));
    std::string digits;
    for (char c : mantissa)
        if (c != '.') digits += c;
    int point = 1 + exponent;  // digits before the decimal point
    std::string integer, fraction;
    if (point <= 0) {
        integer = "0";
        fraction = std::string(static_cast<std::size_t>(-point), '0') + digits;
    } else if (static_cast<std::size_t>(point) >= digits.size()) {
        integer = digits + std::string(static_cast<std::size_t>(point) - digits.size(), '0');
    } else {
        integer = digits.substr(0, static_cast<std::size_t>(point));
        fraction = digits.substr(static_cast<std::size_t>(point));
    }
    while (!fraction.empty() && fraction.back() == '0') fraction.pop_back();
    if (fraction.empty()) fraction = "0";
    return (negative ? "-" : "") + integer + "." + fraction;
}

inline std::string two(unsigned value) {
    char buffer[8];
    std::snprintf(buffer, sizeof buffer, "%02u", value);
    return buffer;
}

inline std::string date_text(int year, unsigned month, unsigned day) {
    char buffer[32];
    std::snprintf(buffer, sizeof buffer, "%04d-%02u-%02u", year, month, day);
    return buffer;
}

// Fraction keeps only significant digits and is omitted when zero.
inline std::string time_text(unsigned hour, unsigned minute, unsigned second, uint32_t nanosecond) {
    std::string text = two(hour) + ":" + two(minute) + ":" + two(second);
    if (nanosecond) {
        char buffer[16];
        std::snprintf(buffer, sizeof buffer, "%09u", static_cast<unsigned>(nanosecond));
        std::string fraction = buffer;
        while (!fraction.empty() && fraction.back() == '0') fraction.pop_back();
        text += "." + fraction;
    }
    return text;
}

// Howard Hinnant's days_from_civil / civil_from_days (proleptic Gregorian).
inline int64_t days_from_civil(int64_t y, unsigned m, unsigned d) {
    y -= m <= 2;
    const int64_t era = (y >= 0 ? y : y - 399) / 400;
    const unsigned yoe = static_cast<unsigned>(y - era * 400);
    const unsigned doy = (153 * (m > 2 ? m - 3 : m + 9) + 2) / 5 + d - 1;
    const unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return era * 146097 + static_cast<int64_t>(doe) - 719468;
}

inline void civil_from_days(int64_t z, int64_t &y, unsigned &m, unsigned &d) {
    z += 719468;
    const int64_t era = (z >= 0 ? z : z - 146096) / 146097;
    const unsigned doe = static_cast<unsigned>(z - era * 146097);
    const unsigned yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    const unsigned doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    const unsigned mp = (5 * doy + 2) / 153;
    d = doy - (153 * mp + 2) / 5 + 1;
    m = mp < 10 ? mp + 3 : mp - 9;
    y = static_cast<int64_t>(yoe) + era * 400 + (m <= 2);
}

// Offset date-time fields -> UTC instant YYYY-MM-DDTHH:MM:SS[.fraction]Z.
inline std::string utc_instant(int year, unsigned month, unsigned day, unsigned hour,
                               unsigned minute, unsigned second, uint32_t nanosecond,
                               int offset_minutes) {
    int64_t seconds = days_from_civil(year, month, day) * 86400 + hour * 3600 + minute * 60 + second
                      - static_cast<int64_t>(offset_minutes) * 60;
    int64_t days = seconds >= 0 ? seconds / 86400 : (seconds - 86399) / 86400;
    int64_t rest = seconds - days * 86400;
    int64_t y;
    unsigned m, d;
    civil_from_days(days, y, m, d);
    return date_text(static_cast<int>(y), m, d) + "T" +
           time_text(static_cast<unsigned>(rest / 3600), static_cast<unsigned>(rest % 3600 / 60),
                     static_cast<unsigned>(rest % 60), nanosecond) + "Z";
}

}  // namespace parsarium

#endif
