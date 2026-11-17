#include "harness.h"

#include <cxxtools/utf8codec.h>
#include <cxxtools/xml/attribute.h>
#include <cxxtools/xml/characters.h>
#include <cxxtools/xml/node.h>
#include <cxxtools/xml/startelement.h>
#include <cxxtools/xml/xmlreader.h>

#include <algorithm>
#include <cstdio>
#include <exception>
#include <sstream>
#include <string>
#include <vector>

// Raw-name summary of cxxtools' XmlReader pull events. XmlReader reports
// element and attribute names as written (prefix:local) and keeps xmlns and
// xmlns:* declarations as ordinary attributes in source order; it never fills
// the StartElement's NamespaceContext, so no namespace URI is reported and the
// adapter resolves nothing itself.

namespace {

std::string utf8(const cxxtools::String &text) { return cxxtools::Utf8Codec::encode(text); }

void flush(std::string *run, std::vector<std::string> *text) {
    size_t start = run->find_first_not_of(" \t\r\n");
    if (start != std::string::npos) {
        size_t end = run->find_last_not_of(" \t\r\n");
        text->push_back(run->substr(start, end - start + 1));
    }
    run->clear();
}

void quote(std::string *out, const std::string &s) {
    out->push_back('"');
    for (unsigned char c : s) {
        if (c == '"' || c == '\\') { out->push_back('\\'); out->push_back(static_cast<char>(c)); }
        else if (c < 0x20) { char esc[8]; std::snprintf(esc, sizeof(esc), "\\u%04x", c); out->append(esc); }
        else out->push_back(static_cast<char>(c));
    }
    out->push_back('"');
}

void array(std::string *out, const char *key, const std::vector<std::string> &items) {
    quote(out, key);
    out->append(":[");
    for (size_t i = 0; i < items.size(); i++) {
        if (i) out->push_back(',');
        quote(out, items[i]);
    }
    out->push_back(']');
}

}  // namespace

int parsarium_parse_xml(const uint8_t *data, size_t size, std::string *json) {
    if (!data || !json || size == 0 || size > (1u << 20)) return 0;
    std::vector<std::string> elements, attributes, text;
    std::string run;
    int depth = 0, max_depth = 0;
    try {
        // Documented pull API: XmlReader over a std::istream of the local bytes; get() then next().
        std::istringstream input(std::string(reinterpret_cast<const char *>(data), size));
        cxxtools::xml::XmlReader reader(input);
        for (const cxxtools::xml::Node *node = &reader.get();
             node->type() != cxxtools::xml::Node::EndDocument; node = &reader.next()) {
            switch (node->type()) {
            case cxxtools::xml::Node::StartElement: {
                flush(&run, &text);
                auto &element = static_cast<const cxxtools::xml::StartElement &>(*node);
                max_depth = std::max(max_depth, ++depth);
                elements.push_back(utf8(element.name()));
                for (const auto &attribute : element.attributes())
                    attributes.push_back(utf8(attribute.name()) + "=" + utf8(attribute.value()));
                break;
            }
            case cxxtools::xml::Node::EndElement:
                flush(&run, &text);
                depth--;
                break;
            case cxxtools::xml::Node::Characters:
                run += utf8(static_cast<const cxxtools::xml::Characters &>(*node).content());
                break;
            default:
                flush(&run, &text);
                break;
            }
        }
    } catch (const std::exception &) {
        return 0;
    }
    flush(&run, &text);
    if (elements.empty() || depth != 0) return 0;
    std::string out = "{";
    array(&out, "attributes", attributes);
    out.push_back(',');
    array(&out, "elements", elements);
    out += ",\"max_depth\":" + std::to_string(max_depth) + ",\"root\":";
    quote(&out, elements.front());
    out.push_back(',');
    array(&out, "text", text);
    out.push_back('}');
    *json = out;
    return 1;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    std::string json;
    (void)parsarium_parse_xml(data, size, &json);
    return 0;
}
