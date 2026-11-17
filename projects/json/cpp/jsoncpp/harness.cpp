#include "harness.h"

#include <json/json.h>

#include <algorithm>
#include <memory>

static void walk(const Json::Value &value, int64_t depth,
                 parsarium_json_result *result) {
    switch (value.type()) {
    case Json::objectValue:
        result->objects++;
        result->max_depth = std::max(result->max_depth, depth);
        for (const auto &name : value.getMemberNames()) walk(value[name], depth + 1, result);
        break;
    case Json::arrayValue:
        result->arrays++;
        result->max_depth = std::max(result->max_depth, depth);
        for (Json::ArrayIndex i = 0; i < value.size(); i++) walk(value[i], depth + 1, result);
        break;
    case Json::stringValue:
        result->strings.push_back(value.asString());
        break;
    case Json::intValue:
    case Json::uintValue:
    case Json::realValue:
        result->numbers.push_back(value.asDouble());
        break;
    case Json::booleanValue:
        result->booleans++;
        break;
    case Json::nullValue:
        result->nulls++;
        break;
    }
}

int parsarium_parse_json(const uint8_t *data, size_t size,
                         parsarium_json_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    *result = parsarium_json_result();
    // Documented byte-range API: CharReaderBuilder::newCharReader()->parse(begin, end, ...).
    Json::CharReaderBuilder builder;
    Json::CharReaderBuilder::strictMode(&builder.settings_);
    std::unique_ptr<Json::CharReader> reader(builder.newCharReader());
    Json::Value root;
    std::string errors;
    const char *begin = reinterpret_cast<const char *>(data);
    if (!reader->parse(begin, begin + size, &root, &errors)) return 0;
    if (root.isObject()) result->root = "object";
    else if (root.isArray()) result->root = "array";
    else return 0;
    if (root.isObject()) result->top_level_keys = root.getMemberNames();
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
