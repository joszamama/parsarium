#ifndef PARSARIUM_LIBXMLB_XML_H
#define PARSARIUM_LIBXMLB_XML_H
#include <stddef.h>
#include <stdint.h>
/* Canonical raw-name JSON summary of one document from libxmlb's tree; caller frees. */
char *parsarium_parse_xml(const uint8_t *data, size_t size);
/* Why the last parsarium_parse_xml call returned NULL, or "" when libxmlb gave no reason. */
const char *parsarium_xml_error(void);
#endif
