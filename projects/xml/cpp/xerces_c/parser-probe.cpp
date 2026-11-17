#include <xercesc/dom/DOM.hpp>
#include <xercesc/framework/MemBufInputSource.hpp>
#include <xercesc/parsers/XercesDOMParser.hpp>
#include <xercesc/sax/HandlerBase.hpp>
#include <xercesc/util/PlatformUtils.hpp>

#include <fstream>
#include <iterator>
#include <string>

using namespace xercesc;

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    const std::string bytes(std::istreambuf_iterator<char>{file}, {});
    if (bytes.empty() || bytes.size() > (1u << 20)) return 2;
    try {
        XMLPlatformUtils::Initialize();
        XercesDOMParser parser;
        parser.setDoNamespaces(true);
        parser.setValidationScheme(XercesDOMParser::Val_Never);
        parser.setLoadExternalDTD(false);
        parser.setDisableDefaultEntityResolution(true);
        parser.setCreateEntityReferenceNodes(false);
        HandlerBase errors;
        parser.setErrorHandler(&errors);
        MemBufInputSource input(reinterpret_cast<const XMLByte*>(bytes.data()),
                                bytes.size(), "parsarium-input", false);
        parser.parse(input);
        const DOMDocument* document = parser.getDocument();
        return parser.getErrorCount() == 0 && document && document->getDocumentElement() ? 0 : 1;
    } catch (...) {
        return 1;
    }
}
