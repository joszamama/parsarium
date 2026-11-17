#ifndef PARSARIUM_RAPIDYAML_HARNESS_H
#define PARSARIUM_RAPIDYAML_HARNESS_H

#include <stddef.h>
#include <stdint.h>

#include <string>

// Parses one YAML document from local bytes with ryml::parse_in_arena and
// writes the Parsarium typed tree as compact JSON. Returns 0 on parse failure
// or on a node outside the tested subset (explicit tags, several documents).
int parsarium_parse_yaml(const uint8_t *data, size_t size, std::string *tree_json);

#endif
