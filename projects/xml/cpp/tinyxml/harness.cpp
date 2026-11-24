#include "harness.h"

#include <tinyxml.h>

#include <algorithm>
#include <cstring>
#include <map>
#include <set>

// TinyXML (version 1, 2.6.2) preserves qualified names and does no namespace
// processing. Resolve namespace declarations from the parsed attributes for a
// comparable namespace-aware control result; the expanded names are adapter
// output over TinyXML's tree, as for the TinyXML2, pugixml and RapidXML paths.
using scope_map = std::map<std::string, std::string>;
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
        auto found = scope.find(prefix);
        if (found != scope.end()) uri = found->second;
        else if (colon) return false;
    }
    if (uri.empty()) *out = local;
    else { uris->insert(uri); *out = "{" + uri + "}" + local; }
    return true;
}

static bool walk(const TiXmlElement *element, scope_map scope, int64_t depth,
                 parsarium_xml_result *result, std::set<std::string> *uris) {
    result->max_depth = std::max(result->max_depth, depth);
    for (auto attribute = element->FirstAttribute(); attribute; attribute = attribute->Next()) {
        const char *name = attribute->Name();
        if (std::strcmp(name, "xmlns") == 0) {
            scope[""] = attribute->Value();
            result->namespace_declarations++;
        } else if (std::strncmp(name, "xmlns:", 6) == 0) {
            if (!*attribute->Value()) return false;
            scope[name + 6] = attribute->Value();
            result->namespace_declarations++;
        }
    }
    std::string name;
    if (!expanded(element->Value(), scope, false, uris, &name)) return false;
    result->elements.push_back(name);
    std::vector<std::string> own;
    std::set<std::string> seen;
    for (auto attribute = element->FirstAttribute(); attribute; attribute = attribute->Next()) {
        const char *qname = attribute->Name();
        if (std::strcmp(qname, "xmlns") == 0 || std::strncmp(qname, "xmlns:", 6) == 0) continue;
        std::string key;
        if (!expanded(qname, scope, true, uris, &key)) return false;
        if (!seen.insert(key).second) return false;
        own.push_back(key + "=" + attribute->Value());
    }
    std::sort(own.begin(), own.end());
    result->attributes.insert(result->attributes.end(), own.begin(), own.end());
    // Text and CDATA children are TiXmlText nodes (CDATA() tells them apart).
    std::string text;
    for (auto child = element->FirstChild(); child; child = child->NextSibling()) {
        if (auto node = child->ToText()) text += node->Value();
    }
    if (text.find_first_not_of(" \t\r\n") != std::string::npos) result->text.push_back(text);
    for (auto child = element->FirstChildElement(); child; child = child->NextSiblingElement()) {
        if (!walk(child, scope, depth + 1, result, uris)) return false;
    }
    return true;
}

int parsarium_parse_xml(const uint8_t *data, size_t size,
                        parsarium_xml_result *result, std::string *error) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    *result = parsarium_xml_result();
    // TiXmlDocument::Parse takes a NUL-terminated string, so input stops at the first NUL byte.
    std::string text(reinterpret_cast<const char *>(data), size);
    TiXmlDocument document;
    document.Parse(text.c_str(), nullptr, TIXML_ENCODING_UTF8);
    if (document.Error()) {
        if (error) *error = std::string("TiXmlDocument::Parse failed: ") + document.ErrorDesc() + " (id " +
                            std::to_string(document.ErrorId()) + ", row " + std::to_string(document.ErrorRow()) +
                            ", column " + std::to_string(document.ErrorCol()) + ")";
        return 0;
    }
    const TiXmlElement *root = document.RootElement();
    if (!root) {
        if (error) *error = "TiXmlDocument::Parse returned a document without a root element";
        return 0;
    }
    std::set<std::string> uris;
    if (!walk(root, scope_map(), 1, result, &uris)) {
        *result = parsarium_xml_result();
        if (error) *error = "names are not namespace-well-formed (unbound prefix, empty prefix binding or repeated expanded attribute)";
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
