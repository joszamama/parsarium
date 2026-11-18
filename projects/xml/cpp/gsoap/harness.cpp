#include "harness.h"

#include "soapH.h"
#include "soap.nsmap"

#include <algorithm>
#include <cstring>
#include <set>
#include <sstream>

// gSOAP's DOM parser (dom.cpp over the stdsoap2.cpp XML engine) is namespace
// aware: each soap_dom_element and soap_dom_attribute carries the namespace
// URI it resolved (nstr) next to the qualified name as written (name). The
// parser keeps xmlns and xmlns:* declarations as DOM attributes with no
// namespace. The adapter only splits the local part off the qualified name;
// URIs, declarations and text come from the DOM.

static std::string local_name(const char *qname) {
    const char *colon = std::strchr(qname, ':');
    return colon ? std::string(colon + 1) : std::string(qname);
}

static std::string expanded(const char *nstr, const char *qname) {
    if (nstr && *nstr) return std::string("{") + nstr + "}" + local_name(qname);
    return local_name(qname);
}

static bool is_declaration(const char *qname) {
    return std::strcmp(qname, "xmlns") == 0 || std::strncmp(qname, "xmlns:", 6) == 0;
}

static void add_text(const char *text, parsarium_xml_result *result) {
    if (!text) return;
    std::string run(text);
    size_t first = run.find_first_not_of(" \t\r\n");
    if (first == std::string::npos) return;
    size_t last = run.find_last_not_of(" \t\r\n");
    result->text.push_back(run.substr(first, last - first + 1));
}

static bool walk(const soap_dom_element *element, int64_t depth,
                 parsarium_xml_result *result, std::set<std::string> *uris) {
    if (!element->name) return false;
    result->max_depth = std::max(result->max_depth, depth);
    result->elements.push_back(expanded(element->nstr, element->name));
    std::vector<std::string> own;
    for (const soap_dom_attribute *attribute = element->atts; attribute; attribute = attribute->next) {
        const char *value = attribute->text ? attribute->text : "";
        if (is_declaration(attribute->name)) {
            result->namespace_declarations++;
            if (*value) uris->insert(value);
            continue;
        }
        own.push_back(expanded(attribute->nstr, attribute->name) + "=" + value);
    }
    std::sort(own.begin(), own.end());
    result->attributes.insert(result->attributes.end(), own.begin(), own.end());
    // A text-only element keeps its character data in text; with element
    // children, each run of character data is an unnamed child node.
    add_text(element->text, result);
    for (const soap_dom_element *child = element->elts; child; child = child->next) {
        if (!child->name) {
            add_text(child->text, result);
        } else if (!walk(child, depth + 1, result, uris)) {
            return false;
        }
    }
    return true;
}

int parsarium_parse_xml(const uint8_t *data, size_t size,
                        parsarium_xml_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    *result = parsarium_xml_result();
    std::istringstream in(std::string(reinterpret_cast<const char *>(data), size));
    soap *ctx = soap_new1(SOAP_C_UTFSTRING | SOAP_DOM_TREE);
    if (!ctx) return 0;
    int ok = 0;
    {
        xsd__anyType dom(ctx);
        in >> dom;
        if (!ctx->error) {
            std::set<std::string> uris;
            ok = walk(&dom, 1, result, &uris);
            if (ok) {
                result->root = result->elements.front();
                result->namespaces.assign(uris.begin(), uris.end());
            }
        }
    }
    if (!ok) *result = parsarium_xml_result();
    soap_destroy(ctx);
    soap_end(ctx);
    soap_free(ctx);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parsarium_xml_result result;
    (void)parsarium_parse_xml(data, size, &result);
    return 0;
}
