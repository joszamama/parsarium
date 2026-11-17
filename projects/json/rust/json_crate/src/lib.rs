use std::error::Error;

use json::JsonValue;

#[derive(Default)]
struct Summary {
    objects: u64,
    arrays: u64,
    booleans: u64,
    nulls: u64,
    max_depth: u64,
    numbers: Vec<f64>,
    strings: Vec<String>,
}

impl Summary {
    fn walk(&mut self, value: &JsonValue, depth: u64) -> Result<(), Box<dyn Error>> {
        match value {
            JsonValue::Object(map) => {
                self.objects += 1;
                self.max_depth = self.max_depth.max(depth + 1);
                for (_, child) in map.iter() {
                    self.walk(child, depth + 1)?;
                }
            }
            JsonValue::Array(items) => {
                self.arrays += 1;
                self.max_depth = self.max_depth.max(depth + 1);
                for child in items.iter() {
                    self.walk(child, depth + 1)?;
                }
            }
            JsonValue::Short(_) | JsonValue::String(_) => {
                self.strings
                    .push(value.as_str().ok_or("missing string")?.to_string());
            }
            JsonValue::Boolean(_) => self.booleans += 1,
            JsonValue::Null => self.nulls += 1,
            JsonValue::Number(_) => self.numbers.push(value.as_f64().ok_or("missing number")?),
        }
        Ok(())
    }
}

/// Decode local UTF-8 JSON text with json-rust's own parser. serde_json only
/// encodes the observed structural summary.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let value = json::parse(text)?;
    let root = match &value {
        JsonValue::Object(_) => "object",
        JsonValue::Array(_) => "array",
        JsonValue::Short(_) | JsonValue::String(_) => "string",
        JsonValue::Number(_) => "number",
        JsonValue::Boolean(_) => "boolean",
        JsonValue::Null => "null",
    };
    let mut summary = Summary::default();
    summary.walk(&value, 0)?;
    summary.numbers.sort_by(f64::total_cmp);
    summary.strings.sort();
    let mut keys: Vec<String> = value.entries().map(|(key, _)| key.to_string()).collect();
    keys.sort();
    Ok(serde_json::json!({"root": root, "objects": summary.objects,
                          "arrays": summary.arrays, "booleans": summary.booleans,
                          "nulls": summary.nulls, "max_depth": summary.max_depth,
                          "numbers": summary.numbers, "strings": summary.strings,
                          "top_level_keys": keys}))
}
