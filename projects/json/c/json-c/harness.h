#ifndef PARSARIUM_JSON_C_JSON_HARNESS_H
#define PARSARIUM_JSON_C_JSON_HARNESS_H

#include <stddef.h>
#include <stdint.h>

#include <json.h>

/* Parse one complete local JSON byte buffer with json_tokener_parse_ex. Returns
 * nonzero on success; *out is NULL for a JSON null root. */
int parsarium_parse_json(const uint8_t *data, size_t size, struct json_object **out);

/* Why the last parsarium_parse_json call failed, or "" when json-c gave no reason. */
const char *parsarium_json_error(void);

/* Print the cross-ecosystem control summary for a parsed value. */
void parsarium_print_summary(struct json_object *root);

/* Print the full parsed value as canonical JSON from json-c's tree. */
void parsarium_print_tree(struct json_object *value);

#endif
