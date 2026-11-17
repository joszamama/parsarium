#include "harness.h"

#include <libxml++/libxml++.h>
#include <libxml/tree.h>

#include <algorithm>
#include <set>
#include <string>
#include <vector>

static std::string expanded(const xmlpp::Node* node, std::set<std::string>* uris) {
    const std::string name = node->get_name2().value_or("");
    const std::string uri = node->get_namespace_uri2().value_or("");
    if (uri.empty()) return name;
    uris->insert(uri);
    return "{" + uri + "}" + name;
}

static bool walk(const xmlpp::Element* element, int64_t depth,
                 parsarium_xml_result* result, std::set<std::string>* uris) {
    if (!element) return false;
    result->max_depth = std::max(result->max_depth, depth);
    result->elements.push_back(expanded(element, uris));
    // libxml++ exposes the libxml2 DOM object. Namespace declarations are
    // separate from attributes in that DOM and have no wrapper list API.
    for (const xmlNs* ns = element->cobj()->nsDef; ns; ns = ns->next)
        ++result->namespace_declarations;
    std::vector<std::string> own;
    for (const xmlpp::Attribute* attr : element->get_attributes())
        own.push_back(expanded(attr, uris) + "=" + attr->get_value2().value_or(""));
    std::sort(own.begin(), own.end());
    result->attributes.insert(result->attributes.end(), own.begin(), own.end());

    std::string text;
    for (const xmlpp::Node* child : element->get_children()) {
        if (const auto* content = dynamic_cast<const xmlpp::TextNode*>(child))
            text += content->get_content2().value_or("");
        else if (const auto* cdata = dynamic_cast<const xmlpp::CdataNode*>(child))
            text += cdata->get_content2().value_or("");
    }
    if (text.find_first_not_of(" \t\r\n") != std::string::npos)
        result->text.push_back(text);
    for (const xmlpp::Node* child : element->get_children()) {
        if (const auto* nested = dynamic_cast<const xmlpp::Element*>(child)) {
            if (!walk(nested, depth + 1, result, uris)) return false;
        }
    }
    return true;
}

int parsarium_parse_xml(const uint8_t* data, size_t size,
                        parsarium_xml_result* result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    *result = parsarium_xml_result();
    try {
        xmlpp::DomParser parser;
        parser.set_parser_options(XML_PARSE_NONET,
                                  XML_PARSE_DTDVALID | XML_PARSE_NOENT | XML_PARSE_DTDLOAD);
        // This is libxml++'s documented local byte-buffer input API.
        parser.parse_memory_raw(data, size);
        const xmlpp::Document* document = parser.get_document();
        const xmlpp::Element* root = document ? document->get_root_node() : nullptr;
        std::set<std::string> uris;
        if (!walk(root, 1, result, &uris)) return 0;
        result->root = result->elements.front();
        result->namespaces.assign(uris.begin(), uris.end());
        return 1;
    } catch (const std::exception&) {
        *result = parsarium_xml_result();
        return 0;
    }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
    parsarium_xml_result result;
    (void)parsarium_parse_xml(data, size, &result);
    return 0;
}
