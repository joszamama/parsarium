#ifndef PARSARIUM_RESVG_CPP_HARNESS_H
#define PARSARIUM_RESVG_CPP_HARNESS_H
#include <array>
#include <cstddef>
#include <cstdint>
#include <optional>

struct parsarium_svg_result {
    unsigned width = 0, height = 0;
    std::array<unsigned char, 3> first{};
    std::optional<std::array<unsigned char, 3>> second;
};

// Parses one SVG through resvg_parse_tree_from_file on a private local file and
// renders it to RGBA. Returns false unless usvg produced a bounded, non-empty size.
bool parsarium_parse_svg(const std::uint8_t *data, std::size_t size, parsarium_svg_result &result);
#endif
