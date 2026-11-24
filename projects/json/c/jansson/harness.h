#ifndef PARSARIUM_JANSSON_JSON_HARNESS_H
#define PARSARIUM_JANSSON_JSON_HARNESS_H

#include <stddef.h>
#include <stdint.h>

#include <jansson.h>

/* Parse one complete local JSON byte buffer with json_loadb. */
json_t *parsarium_parse_json(const uint8_t *data, size_t size);

/* Why the last parsarium_parse_json call returned NULL, or "" when jansson gave no reason. */
const char *parsarium_json_error(void);

/* Print the cross-ecosystem control summary for a parsed value. */
void parsarium_print_summary(json_t *root);

/* Print the full parsed value as canonical JSON from jansson's tree. */
void parsarium_print_tree(json_t *value);

#endif
