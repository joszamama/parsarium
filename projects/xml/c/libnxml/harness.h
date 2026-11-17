#ifndef PARSARIUM_LIBNXML_XML_H
#define PARSARIUM_LIBNXML_XML_H
#include <stddef.h>
#include <stdint.h>
/* Canonical raw-name JSON summary of one document from libnxml's tree; caller frees. */
char *parsarium_parse_xml(const uint8_t *data, size_t size);
#endif
