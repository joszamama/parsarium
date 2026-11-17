#include "harness.h"
#include <rapidxml.hpp>

#include <algorithm>
#include <cstring>
#include <map>
#include <set>
#include <string>
#include <vector>

using scope_map = std::map<std::string, std::string>;

static bool expanded(const std::string &qname, const scope_map &scope, bool attribute,
                     std::set<std::string> *uris, std::string *out) {
    size_t colon = qname.find(':');
    std::string prefix = colon == std::string::npos ? "" : qname.substr(0, colon);
    std::string local = colon == std::string::npos ? qname : qname.substr(colon + 1);
    if (local.empty() || (colon != std::string::npos &&
        (prefix.empty() || local.find(':') != std::string::npos))) return false;
    std::string uri;
    if (prefix == "xml") uri = "http://www.w3.org/XML/1998/namespace";
    else if (colon != std::string::npos || !attribute) {
        auto found = scope.find(prefix);
        if (found != scope.end()) uri = found->second;
        else if (colon != std::string::npos) return false;
    }
    if (uri.empty()) *out = local;
    else { uris->insert(uri); *out = "{" + uri + "}" + local; }
    return true;
}

static bool walk(const rapidxml::xml_node<> *element, scope_map scope, int64_t depth,
                 parsarium_xml_result *result, std::set<std::string> *uris) {
    result->max_depth = std::max(result->max_depth, depth);
    for (auto *attribute = element->first_attribute(); attribute; attribute = attribute->next_attribute()) {
        std::string name(attribute->name(), attribute->name_size());
        std::string value(attribute->value(), attribute->value_size());
        if (name == "xmlns") { scope[""] = value; ++result->namespace_declarations; }
        else if (name.compare(0, 6, "xmlns:") == 0) {
            if (value.empty()) return false;
            scope[name.substr(6)] = value;
            ++result->namespace_declarations;
        }
    }
    std::string name;
    if (!expanded(std::string(element->name(), element->name_size()), scope, false, uris, &name))
        return false;
    result->elements.push_back(name);
    std::vector<std::string> own;
    std::set<std::string> seen;
    for (auto *attribute = element->first_attribute(); attribute; attribute = attribute->next_attribute()) {
        std::string qname(attribute->name(), attribute->name_size());
        if (qname == "xmlns" || qname.compare(0, 6, "xmlns:") == 0) continue;
        std::string key;
        if (!expanded(qname, scope, true, uris, &key) || !seen.insert(key).second) return false;
        own.push_back(key + "=" + std::string(attribute->value(), attribute->value_size()));
    }
    std::sort(own.begin(), own.end());
    result->attributes.insert(result->attributes.end(), own.begin(), own.end());
    std::string text;
    for (auto *child = element->first_node(); child; child = child->next_sibling()) {
        if (child->type() == rapidxml::node_data || child->type() == rapidxml::node_cdata)
            text.append(child->value(), child->value_size());
    }
    if (text.find_first_not_of(" \t\r\n") != std::string::npos) result->text.push_back(text);
    for (auto *child = element->first_node(); child; child = child->next_sibling())
        if (child->type() == rapidxml::node_element &&
            !walk(child, scope, depth + 1, result, uris)) return false;
    return true;
}

int parsarium_parse_xml(const uint8_t *data, size_t size, parsarium_xml_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20) ||
        std::memchr(data, 0, size)) return 0;
    *result = parsarium_xml_result();
    std::vector<char> buffer(data, data + size);
    buffer.push_back('\0');
    rapidxml::xml_document<> document;
    try { document.parse<0>(buffer.data()); }
    catch (const rapidxml::parse_error &) { return 0; }
    const rapidxml::xml_node<> *root = nullptr;
    for (auto *node = document.first_node(); node; node = node->next_sibling())
        if (node->type() == rapidxml::node_element) { root = node; break; }
    if (!root) return 0;
    std::set<std::string> uris;
    if (!walk(root, scope_map(), 1, result, &uris)) {
        *result = parsarium_xml_result();
        return 0;
    }
    result->root = result->elements.front();
    result->namespaces.assign(uris.begin(), uris.end());
    return 1;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parsarium_xml_result result;
    (void)parsarium_parse_xml(data, size, &result);
    return 0;
}
