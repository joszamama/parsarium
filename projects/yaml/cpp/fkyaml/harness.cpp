#include "harness.h"

#include <ios>  // the v0.5.0 headers use std::streamsize without including <ios>

#include <fkYAML/node.hpp>
#include <fkYAML/ordered_map.hpp>

#include <charconv>
#include <cstdio>
#include <exception>
#include <vector>

// fkYAML resolves plain scalars itself (YAML 1.2 core schema: null, bool,
// int, float, string) and expands aliases to their anchored node through
// basic_node's reference resolution. The harness only walks the returned tree
// and prints it; it does no typing, escape decoding, block folding or alias
// handling of its own. fkyaml::ordered_map keeps mapping keys in source order
// (the default fkyaml::node uses std::map).
namespace {

using node_t = fkyaml::basic_node<std::vector, fkyaml::ordered_map>;

void string_json(const std::string &text, std::string *out) {
    out->push_back('"');
    for (unsigned char c : text) {
        if (c == '"' || c == '\\') {
            out->push_back('\\');
            out->push_back(static_cast<char>(c));
        } else if (c < 0x20) {
            char buffer[8];
            std::snprintf(buffer, sizeof buffer, "\\u%04x", c);
            out->append(buffer);
        } else {
            out->push_back(static_cast<char>(c));  // UTF-8 passes through
        }
    }
    out->push_back('"');
}

void tagged(const char *kind, const std::string &text, std::string *out) {
    out->append("[\"").append(kind).append("\",");
    string_json(text, out);
    out->push_back(']');
}

bool emit(const node_t &n, int depth, std::string *out) {
    if (depth > 64 || n.has_tag_name()) return false;
    if (n.is_mapping()) {
        out->append("[\"map\",[");
        bool first = true;
        for (const auto &entry : n.as_map()) {
            if (!entry.first.is_string() || entry.first.has_tag_name()) return false;
            if (!first) out->push_back(',');
            first = false;
            out->push_back('[');
            string_json(entry.first.as_str(), out);
            out->push_back(',');
            if (!emit(entry.second, depth + 1, out)) return false;
            out->push_back(']');
        }
        out->append("]]");
        return true;
    }
    if (n.is_sequence()) {
        out->append("[\"seq\",[");
        bool first = true;
        for (const auto &child : n.as_seq()) {
            if (!first) out->push_back(',');
            first = false;
            if (!emit(child, depth + 1, out)) return false;
        }
        out->append("]]");
        return true;
    }
    if (n.is_null()) {
        out->append("[\"null\"]");
    } else if (n.is_boolean()) {
        out->append(n.as_bool() ? "[\"bool\",true]" : "[\"bool\",false]");
    } else if (n.is_integer()) {
        tagged("int", std::to_string(n.as_int()), out);
    } else if (n.is_float_number()) {
        char buffer[64];
        auto result = std::to_chars(buffer, buffer + sizeof buffer, n.as_float());
        if (result.ec != std::errc()) return false;
        tagged("float", std::string(buffer, result.ptr), out);
    } else if (n.is_string()) {
        tagged("str", n.as_str(), out);
    } else {
        return false;
    }
    return true;
}

}  // namespace

int parsarium_parse_yaml(const uint8_t *data, size_t size, std::string *tree_json) {
    if (!data || !tree_json || size == 0 || size > (1u << 20)) return 0;
    tree_json->clear();
    try {
        // Documented API: basic_node::deserialize(ItrType begin, ItrType end)
        // (https://fktn-k.github.io/fkYAML/api/basic_node/deserialize/).
        const char *begin = reinterpret_cast<const char *>(data);
        node_t root = node_t::deserialize(begin, begin + size);
        return emit(root, 0, tree_json) ? 1 : 0;
    } catch (const std::exception &) {
        return 0;
    }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    std::string tree;
    (void)parsarium_parse_yaml(data, size, &tree);
    return 0;
}
