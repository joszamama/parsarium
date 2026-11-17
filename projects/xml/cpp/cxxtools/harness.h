#ifndef PARSARIUM_CXXTOOLS_XML_HARNESS_H
#define PARSARIUM_CXXTOOLS_XML_HARNESS_H

#include <stddef.h>
#include <stdint.h>

#include <string>

// Canonical raw-name JSON summary of one document from cxxtools' XmlReader; returns 0 on failure.
int parsarium_parse_xml(const uint8_t *data, size_t size, std::string *json);

#endif
