#include "harness.h"

#include <cutl/xml/parser.hxx>

#include <algorithm>
#include <set>
#include <sstream>

// cutl::xml::parser is libcutl's pull parser over Expat in namespace mode.
// Element and attribute qnames carry the namespace URI Expat resolved;
// receive_namespace_decls reports each xmlns/xmlns:* declaration as a
// start_namespace_decl event (its qname holds the bound URI). The adapter
// only formats these events; it resolves nothing itself.

using cutl::xml::parser;

// Expat salts its hash tables from arc4random_buf (glibc >= 2.36) for every
// parser. cutl::xml::parser creates the XML_Parser internally and exposes no
// XML_SetHashSalt hook, so this binary supplies a fixed arc4random_buf, which
// only Expat's salt generation calls; it plays the role of the fixed
// XML_SetHashSalt in the C expat path and makes repeated AFL++ maps
// comparable. Parsing results do not depend on the salt.
extern "C" void arc4random_buf(void *buffer, size_t size) {
    unsigned char *bytes = static_cast<unsigned char *>(buffer);
    for (size_t i = 0; i < size; i++) bytes[i] = static_cast<unsigned char>(0x50 + (i % 8));
}

static std::string expanded(const cutl::xml::qname &name) {
    if (name.namespace_().empty()) return name.name();
    return "{" + name.namespace_() + "}" + name.name();
}

static void flush(std::string *text, parsarium_xml_result *result) {
    size_t first = text->find_first_not_of(" \t\r\n");
    if (first != std::string::npos) {
        size_t last = text->find_last_not_of(" \t\r\n");
        result->text.push_back(text->substr(first, last - first + 1));
    }
    text->clear();
}

int parsarium_parse_xml(const uint8_t *data, size_t size, parsarium_xml_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    *result = parsarium_xml_result();
    std::istringstream input(std::string(reinterpret_cast<const char *>(data), size));
    try {
        parser p(input, "control",
                 parser::receive_elements | parser::receive_characters |
                 parser::receive_attributes_event | parser::receive_namespace_decls);
        std::set<std::string> uris;
        std::vector<std::string> own;
        std::string text;
        int64_t depth = 0;
        bool in_start_tag = false;
        bool in_attribute = false;
        std::string attribute_name, attribute_value;
        auto close_start_tag = [&]() {
            if (!in_start_tag) return;
            std::sort(own.begin(), own.end());
            result->attributes.insert(result->attributes.end(), own.begin(), own.end());
            own.clear();
            in_start_tag = false;
        };
        for (parser::event_type event = p.next(); event != parser::eof; event = p.next()) {
            switch (event) {
            case parser::start_namespace_decl:
                result->namespace_declarations++;
                if (!p.namespace_().empty()) uris.insert(p.namespace_());
                break;
            case parser::end_namespace_decl:
                break;
            case parser::start_element:
                close_start_tag();
                flush(&text, result);
                depth++;
                result->max_depth = std::max(result->max_depth, depth);
                result->elements.push_back(expanded(p.qname()));
                in_start_tag = true;
                break;
            // With receive_attributes_event each attribute is a
            // start_attribute/characters/end_attribute triple.
            case parser::start_attribute:
                attribute_name = expanded(p.qname());
                attribute_value.clear();
                in_attribute = true;
                break;
            case parser::end_attribute:
                own.push_back(attribute_name + "=" + attribute_value);
                in_attribute = false;
                break;
            case parser::characters:
                if (in_attribute) {
                    attribute_value += p.value();
                    break;
                }
                close_start_tag();
                text += p.value();
                break;
            case parser::end_element:
                close_start_tag();
                flush(&text, result);
                depth--;
                break;
            default:
                break;
            }
        }
        close_start_tag();
        if (result->elements.empty()) return 0;
        result->root = result->elements.front();
        result->namespaces.assign(uris.begin(), uris.end());
        return 1;
    } catch (const std::exception &) {
        *result = parsarium_xml_result();
        return 0;
    }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parsarium_xml_result result;
    (void)parsarium_parse_xml(data, size, &result);
    return 0;
}
