#ifndef PARSARIUM_MXML_XML_H
#define PARSARIUM_MXML_XML_H
#include <stddef.h>
#include <stdint.h>
/* Canonical JSON summary of one document, namespaces resolved by the adapter from mxml's tree; caller frees. */
char *parsarium_parse_xml(const uint8_t *data, size_t size);
/* Why the last parsarium_parse_xml call returned NULL, or "" when mxml gave no reason. */
const char *parsarium_xml_error(void);
#endif
