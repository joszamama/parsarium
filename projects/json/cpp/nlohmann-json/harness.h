#ifndef PARSARIUM_NLOHMANN_JSON_HARNESS_H
#define PARSARIUM_NLOHMANN_JSON_HARNESS_H

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

int parsarium_parse_json(const uint8_t *data, size_t size,
                         parsarium_json_result *result);

// After a failed parsarium_parse_json: nlohmann's parse_error text for the same
// bytes (parse() with exceptions enabled), or "" if it gives none.
std::string parsarium_json_error(const uint8_t *data, size_t size);

#endif
