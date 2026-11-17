#include <libxml++/libxml++.h>
#include <libxml/parser.h>

#include <fstream>
#include <iterator>
#include <string>

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 2;
    const std::string bytes(std::istreambuf_iterator<char>{file}, {});
    if (bytes.empty() || bytes.size() > (1u << 20)) return 2;
    try {
        xmlpp::DomParser parser;
        parser.set_parser_options(XML_PARSE_NONET,
                                  XML_PARSE_DTDVALID | XML_PARSE_NOENT | XML_PARSE_DTDLOAD);
        parser.parse_memory_raw(reinterpret_cast<const unsigned char*>(bytes.data()),
                                bytes.size());
        return parser.get_document() && parser.get_document()->get_root_node() ? 0 : 1;
    } catch (const std::exception&) {
        return 1;
    }
}
