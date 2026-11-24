#ifndef PARSARIUM_LIBUCW_XML_H
#define PARSARIUM_LIBUCW_XML_H
#include <stddef.h>
#include <stdint.h>
/* Canonical JSON summary of one namespace-resolved document from LibUCW ucw-xml; caller frees. */
char *parsarium_parse_xml(const uint8_t *data, size_t size);
/* Why the last parsarium_parse_xml call returned NULL, or "" when ucw-xml gave no reason. */
const char *parsarium_xml_error(void);
#endif
