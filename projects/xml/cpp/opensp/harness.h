#ifndef PARSARIUM_OPENSP_XML_HARNESS_H
#define PARSARIUM_OPENSP_XML_HARNESS_H

#include <stddef.h>
#include <stdint.h>

#include <string>
#include <vector>

// Raw-name summary of one document from OpenSP's generic event API.
struct parsarium_xml_result {
    std::string root;
    std::vector<std::string> elements;
    std::vector<std::string> attributes;
    std::vector<std::string> text;
    int64_t max_depth = 0;
};

int parsarium_parse_xml(const uint8_t *data, size_t size, parsarium_xml_result *result);

#endif
