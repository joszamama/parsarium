#include "harness.h"

#include <ryml.hpp>
#include <ryml_std.hpp>

#include <charconv>
#include <cstdio>
#include <exception>
#include <regex>

// rapidyaml keeps every scalar as text plus style bits (plain, single- or
// double-quoted, literal, folded) and reports plain nulls with
// Tree::val_is_null. It has no YAML 1.2 core-schema typing of its own, so this
// adapter types unquoted, non-null scalars with the YAML 1.2 core-schema
// patterns and converts them with c4core's atoi/atod. The controls avoid every
// scalar whose type differs between YAML 1.1 and the 1.2 core schema.
namespace {

const std::regex kBool("true|True|TRUE|false|False|FALSE");
const std::regex kInt("[-+]?[0-9]+");
const std::regex kFloat("[-+]?(\\.[0-9]+|[0-9]+(\\.[0-9]*)?)([eE][-+]?[0-9]+)?");

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

std::string text_of(ryml::csubstr s) { return std::string(s.str ? s.str : "", s.len); }

bool emit(const ryml::Tree &t, ryml::id_type id, int depth, std::string *out) {
    if (depth > 64) return false;
    if (t.is_map(id) || t.is_seq(id)) {
        if (t.has_val_tag(id)) return false;
        const bool map = t.is_map(id);
        out->append(map ? "[\"map\",[" : "[\"seq\",[");
        bool first = true;
        for (ryml::id_type child = t.first_child(id); child != ryml::NONE; child = t.next_sibling(child)) {
            if (!first) out->push_back(',');
            first = false;
            if (map) {
                if (t.has_key_tag(child)) return false;
                out->push_back('[');
                string_json(text_of(t.key(child)), out);
                out->push_back(',');
                if (!emit(t, child, depth + 1, out)) return false;
                out->push_back(']');
            } else if (!emit(t, child, depth + 1, out)) {
                return false;
            }
        }
        out->append("]]");
        return true;
    }
    if (!t.has_val(id) || t.has_val_tag(id)) return false;
    const std::string text = text_of(t.val(id));
    if (t.is_val_quoted(id)) {  // single/double quoted, literal or folded
        tagged("str", text, out);
    } else if (t.val_is_null(id)) {
        out->append("[\"null\"]");
    } else if (std::regex_match(text, kBool)) {
        out->append(text[0] == 't' || text[0] == 'T' ? "[\"bool\",true]" : "[\"bool\",false]");
    } else if (std::regex_match(text, kInt)) {
        long long value = 0;
        ryml::csubstr digits = t.val(id);
        if (!digits.empty() && digits[0] == '+') digits = digits.sub(1);
        if (!c4::atoi(digits, &value)) return false;
        tagged("int", std::to_string(value), out);
    } else if (std::regex_match(text, kFloat)) {
        double value = 0;
        if (!c4::atod(t.val(id), &value)) return false;
        char buffer[64];
        auto result = std::to_chars(buffer, buffer + sizeof buffer, value);
        if (result.ec != std::errc()) return false;
        tagged("float", std::string(buffer, result.ptr), out);
    } else {
        tagged("str", text, out);
    }
    return true;
}

}  // namespace

int parsarium_parse_yaml(const uint8_t *data, size_t size, std::string *tree_json) {
    if (!data || !tree_json || size == 0 || size > (1u << 20)) return 0;
    tree_json->clear();
    try {
        // Documented API: ryml::parse_in_arena(csubstr) in src/c4/yml/parse.hpp;
        // Tree::resolve() expands aliases into copies of the anchored nodes.
        ryml::Tree tree = ryml::parse_in_arena(ryml::csubstr(reinterpret_cast<const char *>(data), size));
        tree.resolve();
        ryml::id_type root = tree.root_id();
        if (tree.is_stream(root)) {
            if (tree.num_children(root) != 1) return 0;
            root = tree.first_child(root);
        }
        return emit(tree, root, 0, tree_json) ? 1 : 0;
    } catch (const std::exception &) {
        return 0;
    }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    std::string tree;
    (void)parsarium_parse_yaml(data, size, &tree);
    return 0;
}
