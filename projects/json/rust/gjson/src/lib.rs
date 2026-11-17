use gjson::Kind;
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

fn walk(raw: &str, depth: u64, summary: &mut Summary) -> bool {
    if depth > 256 {
        return false;
    }
    let value = gjson::parse(raw);
    match value.kind() {
        Kind::Object | Kind::Array => {
            if value.kind() == Kind::Object {
                summary.objects += 1;
            } else {
                summary.arrays += 1;
            }
            summary.max_depth = summary.max_depth.max(depth + 1);
            let mut complete = true;
            value.each(|key, child| {
                if depth == 0 && value.kind() == Kind::Object {
                    summary.top_level_keys.push(key.str().to_string());
                }
                if !walk(child.json(), depth + 1, summary) {
                    complete = false;
                    return false;
                }
                true
            });
            complete
        }
        Kind::Number => {
            summary.numbers.push(value.f64());
            true
        }
        Kind::String => {
            summary.strings.push(value.str().to_string());
            true
        }
        Kind::True | Kind::False => {
            summary.booleans += 1;
            true
        }
        Kind::Null => {
            summary.nulls += 1;
            true
        }
    }
}

/// Validate one complete local JSON text with gjson::valid, then scan its
/// lazy values through gjson::parse and Value::each. serde_json encodes the
/// observable summary only.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    if !gjson::valid(text) {
        return Err("gjson rejected complete JSON text".into());
    }
    let root = match gjson::parse(text).kind() {
        Kind::Object => "object",
        Kind::Array => "array",
        Kind::String => "string",
        Kind::Number => "number",
        Kind::True | Kind::False => "boolean",
        Kind::Null => "null",
    };
    let mut summary = Summary::default();
    if !walk(text, 0, &mut summary) {
        return Err("JSON nesting exceeds harness limit".into());
    }
    summary.numbers.sort_by(f64::total_cmp);
    summary.strings.sort();
    summary.top_level_keys.sort();
    Ok(serde_json::json!({"root": root, "objects": summary.objects,
        "arrays": summary.arrays, "booleans": summary.booleans,
        "nulls": summary.nulls, "max_depth": summary.max_depth,
        "numbers": summary.numbers, "strings": summary.strings,
        "top_level_keys": summary.top_level_keys}))
}
