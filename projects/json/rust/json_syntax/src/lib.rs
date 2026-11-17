use json_syntax::{JsonParse, JsonValue};
use std::error::Error;

#[derive(Default)]
struct Summary {
    objects: u64,
    arrays: u64,
    booleans: u64,
    nulls: u64,
    max_depth: u64,
    numbers: Vec<f64>,
    strings: Vec<String>,
    top_level_keys: Vec<String>,
}

fn walk(value: &JsonValue, depth: u64, summary: &mut Summary) -> Result<(), Box<dyn Error>> {
    if depth > 256 {
        return Err("JSON nesting exceeds harness limit".into());
    }
    match value {
        JsonValue::Object(object) => {
            summary.objects += 1;
            summary.max_depth = summary.max_depth.max(depth + 1);
            for (key, child) in object.iter() {
                if depth == 0 {
                    summary.top_level_keys.push(key.to_string());
                }
                walk(child, depth + 1, summary)?;
            }
        }
        JsonValue::Array(array) => {
            summary.arrays += 1;
            summary.max_depth = summary.max_depth.max(depth + 1);
            for child in array {
                walk(child, depth + 1, summary)?;
            }
        }
        JsonValue::Boolean(_) => summary.booleans += 1,
        JsonValue::Null => summary.nulls += 1,
        JsonValue::Number(number) => summary.numbers.push(number.as_str().parse()?),
        JsonValue::String(string) => summary.strings.push(string.to_string()),
    }
    Ok(())
}

/// Parse one complete local JSON byte slice with json-syntax's own parser.
/// serde_json serializes the resulting summary only.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let (value, _code_map) = JsonValue::parse_slice(data).map_err(|e| format!("{e:?}"))?;
    let root = match value {
        JsonValue::Object(_) => "object",
        JsonValue::Array(_) => "array",
        JsonValue::Boolean(_) => "boolean",
        JsonValue::Null => "null",
        JsonValue::Number(_) => "number",
        JsonValue::String(_) => "string",
    };
    let mut summary = Summary::default();
    walk(&value, 0, &mut summary)?;
    summary.numbers.sort_by(f64::total_cmp);
    summary.strings.sort();
    summary.top_level_keys.sort();
    Ok(serde_json::json!({"root": root, "objects": summary.objects,
        "arrays": summary.arrays, "booleans": summary.booleans,
        "nulls": summary.nulls, "max_depth": summary.max_depth,
        "numbers": summary.numbers, "strings": summary.strings,
        "top_level_keys": summary.top_level_keys}))
}
