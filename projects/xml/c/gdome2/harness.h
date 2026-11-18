#ifndef PARSARIUM_GDOME2_XML_H
#define PARSARIUM_GDOME2_XML_H
#include <stddef.h>
#include <stdint.h>
/* Canonical namespace-resolved JSON summary of one document from the gdome2 DOM; caller frees. */
char *parsarium_parse_xml(const uint8_t *data, size_t size);
#endif
