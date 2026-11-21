#include "harness.h"

#include <nlohmann/json.hpp>

#include <algorithm>

static void walk(const nlohmann::json &value, int64_t depth,
                 parsarium_json_result *result) {
    switch (value.type()) {
    case nlohmann::json::value_t::object:
        result->objects++;
        result->max_depth = std::max(result->max_depth, depth);
        for (const auto &item : value.items()) walk(item.value(), depth + 1, result);
        break;
    case nlohmann::json::value_t::array:
        result->arrays++;
        result->max_depth = std::max(result->max_depth, depth);
        for (const auto &item : value) walk(item, depth + 1, result);
        break;
    case nlohmann::json::value_t::string:
        result->strings.push_back(value.get_ref<const std::string &>());
        break;
    case nlohmann::json::value_t::number_integer:
    case nlohmann::json::value_t::number_unsigned:
    case nlohmann::json::value_t::number_float:
        result->numbers.push_back(value.get<double>());
        break;
    case nlohmann::json::value_t::boolean:
        result->booleans++;
        break;
    case nlohmann::json::value_t::null:
        result->nulls++;
        break;
    default:
        break;
    }
}

int parsarium_parse_json(const uint8_t *data, size_t size,
                         parsarium_json_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    *result = parsarium_json_result();
    // Documented iterator-range API: basic_json::parse(first, last, cb, allow_exceptions, ignore_comments).
    // allow_exceptions=false returns a discarded value on error; comments are rejected.
    nlohmann::json root = nlohmann::json::parse(data, data + size, nullptr, false, false);
    if (root.is_discarded()) return 0;
    if (root.is_object()) result->root = "object";
    else if (root.is_array()) result->root = "array";
    else if (root.is_string()) result->root = "string";
    else if (root.is_number()) result->root = "number";
    else if (root.is_boolean()) result->root = "boolean";
    else result->root = "null";
    if (root.is_object())
        for (const auto &item : root.items()) result->top_level_keys.push_back(item.key());
    walk(root, 1, result);
    std::sort(result->top_level_keys.begin(), result->top_level_keys.end());
    std::sort(result->strings.begin(), result->strings.end());
    std::sort(result->numbers.begin(), result->numbers.end());
    return 1;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parsarium_json_result result;
    (void)parsarium_parse_json(data, size, &result);
    return 0;
}
