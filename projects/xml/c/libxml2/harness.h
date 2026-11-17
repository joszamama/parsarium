#ifndef PARSARIUM_LIBXML2_XML_H
#define PARSARIUM_LIBXML2_XML_H
#include <stddef.h>
#include <stdint.h>
/* Canonical JSON summary of one namespace-resolved document; caller frees. */
char *parsarium_parse_xml(const uint8_t *data, size_t size);
#endif
