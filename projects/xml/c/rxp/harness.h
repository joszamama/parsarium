#ifndef PARSARIUM_RXP_XML_H
#define PARSARIUM_RXP_XML_H
#include <stddef.h>
#include <stdint.h>
/* Canonical JSON summary of one document from RXP with XMLNamespaces on (no declaration count); caller frees. */
char *parsarium_parse_xml(const uint8_t *data, size_t size);
/* Why the last parsarium_parse_xml call returned NULL, or "" when RXP gave no reason. */
const char *parsarium_xml_error(void);
#endif
