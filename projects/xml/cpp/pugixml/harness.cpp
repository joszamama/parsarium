#include "harness.h"

#include <pugixml.hpp>

#include <algorithm>
#include <cstring>
#include <map>
#include <set>

// pugixml keeps qualified names and does no namespace processing; the adapter
// resolves prefixes from in-scope xmlns attributes (Namespaces in XML 1.0).
typedef std::map<std::string, std::string> scope_map;

static const char *const xml_namespace = "http://www.w3.org/XML/1998/namespace";

static bool expanded(const char *qname, const scope_map &scope, bool attribute,
                     std::set<std::string> *uris, std::string *out) {
    const char *colon = std::strchr(qname, ':');
    std::string prefix = colon ? std::string(qname, colon - qname) : std::string();
    std::string local = colon ? std::string(colon + 1) : std::string(qname);
    if (colon && (prefix.empty() || local.empty() || local.find(':') != std::string::npos))
        return false;
    std::string uri;
    if (prefix == "xml") {
        uri = xml_namespace;
    } else if (colon || !attribute) {
        scope_map::const_iterator found = scope.find(prefix);
        if (found != scope.end()) uri = found->second;
        else if (colon) return false;  // unbound prefix
    }
    if (uri.empty()) {
        *out = local;
    } else {
        uris->insert(uri);
        *out = "{" + uri + "}" + local;
    }
    return true;
}

static bool walk(pugi::xml_node element, scope_map scope, int64_t depth,
                 parsarium_xml_result *result, std::set<std::string> *uris) {
    result->max_depth = std::max(result->max_depth, depth);
    for (pugi::xml_attribute attribute = element.first_attribute(); attribute;
         attribute = attribute.next_attribute()) {
        const char *name = attribute.name();
        if (std::strcmp(name, "xmlns") == 0) {
            scope[""] = attribute.value();  // empty value resets the default namespace
            result->namespace_declarations++;
        } else if (std::strncmp(name, "xmlns:", 6) == 0) {
            if (!*attribute.value()) return false;  // prefix undeclaring is XML 1.1 only
            scope[name + 6] = attribute.value();
            result->namespace_declarations++;
        }
    }
    std::string name;
    if (!expanded(element.name(), scope, false, uris, &name)) return false;
    result->elements.push_back(name);
    // Sort each element's attributes by expanded name, as the DOM adapters do.
    std::vector<std::string> own;
    std::set<std::string> seen;
    for (pugi::xml_attribute attribute = element.first_attribute(); attribute;
         attribute = attribute.next_attribute()) {
        const char *qname = attribute.name();
        if (std::strcmp(qname, "xmlns") == 0 || std::strncmp(qname, "xmlns:", 6) == 0) continue;
        std::string key;
        if (!expanded(qname, scope, true, uris, &key)) return false;
        if (!seen.insert(key).second) return false;  // duplicate expanded attribute name
        own.push_back(key + "=" + attribute.value());
    }
    std::sort(own.begin(), own.end());
    result->attributes.insert(result->attributes.end(), own.begin(), own.end());
    std::string text;
    for (pugi::xml_node child = element.first_child(); child; child = child.next_sibling()) {
        if (child.type() == pugi::node_pcdata || child.type() == pugi::node_cdata)
            text += child.value();
    }
    if (text.find_first_not_of(" \t\r\n") != std::string::npos) result->text.push_back(text);
    for (pugi::xml_node child = element.first_child(); child; child = child.next_sibling()) {
        if (child.type() == pugi::node_element &&
            !walk(child, scope, depth + 1, result, uris))
            return false;
    }
    return true;
}

int parsarium_parse_xml(const uint8_t *data, size_t size,
                        parsarium_xml_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    *result = parsarium_xml_result();
    pugi::xml_document document;
    // Documented in-memory byte API: xml_document::load_buffer copies the caller's buffer.
    pugi::xml_parse_result parsed =
        document.load_buffer(data, size, pugi::parse_default, pugi::encoding_utf8);
    if (!parsed) return 0;
    pugi::xml_node root = document.document_element();
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
