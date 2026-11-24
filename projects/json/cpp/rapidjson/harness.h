#ifndef PARSARIUM_RAPIDJSON_HARNESS_H
#define PARSARIUM_RAPIDJSON_HARNESS_H

#include <stddef.h>
#include <stdint.h>

#include <string>
#include <vector>

struct parsarium_json_result {
    std::string root;
    std::vector<std::string> top_level_keys;
    std::vector<std::string> strings;
    std::vector<double> numbers;
    int64_t objects = 0;
    int64_t arrays = 0;
    int64_t booleans = 0;
    int64_t nulls = 0;
    int64_t max_depth = 0;
};

// Returns 0 on failure; *error (when given) then holds RapidJSON's
// GetParseError_En() text and error offset.
int parsarium_parse_json(const uint8_t *data, size_t size,
                         parsarium_json_result *result, std::string *error = nullptr);

#endif
