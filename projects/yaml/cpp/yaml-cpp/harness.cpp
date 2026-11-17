#include "harness.h"

#include <yaml-cpp/yaml.h>

#include <charconv>
#include <cstdio>
#include <regex>

// yaml-cpp resolves plain null scalars itself (NodeType::Null) and marks every
// other scalar with a non-specific tag: "!" for quoted and block scalars, "?"
// for plain scalars. It keeps plain scalars as text, so this adapter types a
// "?" scalar with the YAML 1.2 core-schema patterns and then converts it with
// yaml-cpp's own Node::as<T>. The controls avoid every scalar whose type
// differs between YAML 1.1 and the 1.2 core schema.
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

bool emit(const YAML::Node &node, int depth, std::string *out) {
    if (depth > 64) return false;
    switch (node.Type()) {
    case YAML::NodeType::Null:
        out->append("[\"null\"]");
        return true;
    case YAML::NodeType::Sequence: {
        out->append("[\"seq\",[");
        bool first = true;
        for (const YAML::Node &item : node) {
            if (!first) out->push_back(',');
            first = false;
            if (!emit(item, depth + 1, out)) return false;
        }
        out->append("]]");
        return true;
    }
    case YAML::NodeType::Map: {
        out->append("[\"map\",[");
        bool first = true;
        for (const auto &pair : node) {
            if (pair.first.Type() != YAML::NodeType::Scalar) return false;
            if (!first) out->push_back(',');
            first = false;
            out->push_back('[');
            string_json(pair.first.Scalar(), out);
            out->push_back(',');
            if (!emit(pair.second, depth + 1, out)) return false;
            out->push_back(']');
        }
        out->append("]]");
        return true;
    }
    case YAML::NodeType::Scalar: {
        const std::string &text = node.Scalar();
        if (node.Tag() == "!") {
            tagged("str", text, out);
            return true;
        }
        if (node.Tag() != "?") return false;  // explicit tags are outside the tested subset
        if (std::regex_match(text, kBool)) {
            out->append(node.as<bool>() ? "[\"bool\",true]" : "[\"bool\",false]");
        } else if (std::regex_match(text, kInt)) {
            tagged("int", std::to_string(node.as<long long>()), out);
        } else if (std::regex_match(text, kFloat)) {
            char buffer[64];
            auto result = std::to_chars(buffer, buffer + sizeof buffer, node.as<double>());
            if (result.ec != std::errc()) return false;
            tagged("float", std::string(buffer, result.ptr), out);
        } else {
            tagged("str", text, out);
        }
        return true;
    }
    default:
        return false;
    }
}

}  // namespace

int parsarium_parse_yaml(const uint8_t *data, size_t size, std::string *tree_json) {
    if (!data || !tree_json || size == 0 || size > (1u << 20)) return 0;
    tree_json->clear();
    try {
        // Documented API: YAML::Load(const std::string&) in include/yaml-cpp/node/parse.h.
        YAML::Node root = YAML::Load(std::string(reinterpret_cast<const char *>(data), size));
        return emit(root, 0, tree_json) ? 1 : 0;
    } catch (const YAML::Exception &) {
        return 0;
    }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    std::string tree;
    (void)parsarium_parse_yaml(data, size, &tree);
    return 0;
}
