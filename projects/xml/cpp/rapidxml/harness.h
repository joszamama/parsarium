#ifndef PARSARIUM_TINYXML2_HARNESS_H
#define PARSARIUM_TINYXML2_HARNESS_H

#include <stddef.h>
#include <stdint.h>

#include <string>
#include <vector>

struct parsarium_xml_result {
    std::string root;
    std::vector<std::string> elements;
    std::vector<std::string> attributes;
    std::vector<std::string> namespaces;
    std::vector<std::string> text;
    int64_t namespace_declarations = 0;
    int64_t max_depth = 0;
};

// Returns 0 on failure; *error (when given) then says why (RapidXml's parse_error where it gives one).
int parsarium_parse_xml(const uint8_t *data, size_t size,
                        parsarium_xml_result *result, std::string *error = nullptr);

#endif
