#include "harness.h"

#include <xercesc/dom/DOM.hpp>
#include <xercesc/framework/MemBufInputSource.hpp>
#include <xercesc/parsers/XercesDOMParser.hpp>
#include <xercesc/sax/HandlerBase.hpp>
#include <xercesc/util/PlatformUtils.hpp>
#include <xercesc/util/TransService.hpp>
#include <xercesc/util/XMLUni.hpp>

#include <algorithm>
#include <set>

using namespace xercesc;

static std::string utf8(const XMLCh *text) {
    if (!text) return std::string();
    TranscodeToStr out(text, "UTF-8");
    return std::string(reinterpret_cast<const char *>(out.str()), out.length());
}

static std::string expanded(const DOMNode *node, std::set<std::string> *uris) {
    std::string uri = utf8(node->getNamespaceURI());
    std::string local = utf8(node->getLocalName());
    if (uri.empty()) return local;
    uris->insert(uri);
    return "{" + uri + "}" + local;
}

static void walk(const DOMElement *element, int64_t depth,
                 parsarium_xml_result *result, std::set<std::string> *uris) {
    result->max_depth = std::max(result->max_depth, depth);
    result->elements.push_back(expanded(element, uris));
    // DOM leaves NamedNodeMap order unspecified; sort each element's attributes by name.
    std::vector<std::string> own;
    DOMNamedNodeMap *attributes = element->getAttributes();
    for (XMLSize_t i = 0; i < attributes->getLength(); i++) {
        const DOMNode *attribute = attributes->item(i);
        if (XMLString::equals(attribute->getNamespaceURI(), XMLUni::fgXMLNSURIName)) {
            result->namespace_declarations++;
            continue;
        }
        own.push_back(expanded(attribute, uris) + "=" + utf8(attribute->getNodeValue()));
    }
    std::sort(own.begin(), own.end());
    result->attributes.insert(result->attributes.end(), own.begin(), own.end());
    std::string text;
    for (DOMNode *child = element->getFirstChild(); child; child = child->getNextSibling()) {
        if (child->getNodeType() == DOMNode::TEXT_NODE ||
            child->getNodeType() == DOMNode::CDATA_SECTION_NODE)
            text += utf8(child->getNodeValue());
    }
    if (text.find_first_not_of(" \t\r\n") != std::string::npos) result->text.push_back(text);
    for (DOMElement *child = element->getFirstElementChild(); child;
         child = child->getNextElementSibling())
        walk(child, depth + 1, result, uris);
}

int parsarium_parse_xml(const uint8_t *data, size_t size,
                        parsarium_xml_result *result) {
    static bool initialized = (XMLPlatformUtils::Initialize(), true);
    (void)initialized;
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    *result = parsarium_xml_result();
    XercesDOMParser parser;
    parser.setDoNamespaces(true);
    parser.setValidationScheme(XercesDOMParser::Val_Never);
    parser.setLoadExternalDTD(false);
    parser.setDisableDefaultEntityResolution(true);
    parser.setCreateEntityReferenceNodes(false);
    HandlerBase errors;  // fatalError throws SAXParseException
    parser.setErrorHandler(&errors);
    // Documented in-memory byte API: MemBufInputSource over the caller's buffer.
    MemBufInputSource input(data, size, "parsarium-input", false);
    try {
        parser.parse(input);
    } catch (...) {
        return 0;
    }
    if (parser.getErrorCount() != 0) return 0;
    DOMDocument *document = parser.getDocument();
    DOMElement *root = document ? document->getDocumentElement() : nullptr;
    if (!root) return 0;
    std::set<std::string> uris;
    walk(root, 1, result, &uris);
    result->root = result->elements.front();
    result->namespaces.assign(uris.begin(), uris.end());
    return 1;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parsarium_xml_result result;
    (void)parsarium_parse_xml(data, size, &result);
    return 0;
}
