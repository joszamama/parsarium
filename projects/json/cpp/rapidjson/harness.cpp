#include "harness.h"

#include <rapidjson/document.h>
#include <rapidjson/error/en.h>

#include <algorithm>

static void walk(const rapidjson::Value &value, int64_t depth,
                 parsarium_json_result *result) {
    if (value.IsObject()) {
        result->objects++;
        result->max_depth = std::max(result->max_depth, depth);
        for (auto member = value.MemberBegin(); member != value.MemberEnd(); ++member)
            walk(member->value, depth + 1, result);
    } else if (value.IsArray()) {
        result->arrays++;
        result->max_depth = std::max(result->max_depth, depth);
        for (auto item = value.Begin(); item != value.End(); ++item)
            walk(*item, depth + 1, result);
    } else if (value.IsString()) {
        result->strings.emplace_back(value.GetString(), value.GetStringLength());
    } else if (value.IsNumber()) {
        result->numbers.push_back(value.GetDouble());
    } else if (value.IsBool()) {
        result->booleans++;
    } else if (value.IsNull()) {
        result->nulls++;
    }
}

int parsarium_parse_json(const uint8_t *data, size_t size,
                         parsarium_json_result *result, std::string *error) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    *result = parsarium_json_result();
    rapidjson::Document document;
    // Documented length-bounded in-memory parsing API; default flags are strict.
    document.Parse(reinterpret_cast<const char *>(data), size);
    if (document.HasParseError()) {
        if (error) {
            *error = std::string("rapidjson::Document::Parse failed: ") +
                     rapidjson::GetParseError_En(document.GetParseError()) +
                     " (offset " + std::to_string(document.GetErrorOffset()) + ")";
        }
        return 0;
    }
    if (document.IsObject()) {
        result->root = "object";
        for (auto member = document.MemberBegin(); member != document.MemberEnd(); ++member)
            result->top_level_keys.emplace_back(member->name.GetString(),
                                                member->name.GetStringLength());
    } else if (document.IsArray()) {
        result->root = "array";
    } else if (document.IsString()) {
        result->root = "string";
    } else if (document.IsNumber()) {
        result->root = "number";
    } else if (document.IsBool()) {
        result->root = "boolean";
    } else {
        result->root = "null";
    }
    walk(document, 1, result);
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
