use std::error::Error;

use serde_json::Value;

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
    fn walk(&mut self, value: &Value, depth: u64) -> Result<(), Box<dyn Error>> {
        match value {
            Value::Object(map) => {
                self.objects += 1;
                self.max_depth = self.max_depth.max(depth + 1);
                for child in map.values() {
                    self.walk(child, depth + 1)?;
                }
            }
            Value::Array(items) => {
                self.arrays += 1;
                self.max_depth = self.max_depth.max(depth + 1);
                for child in items {
                    self.walk(child, depth + 1)?;
                }
            }
            Value::String(text) => self.strings.push(text.clone()),
            Value::Number(number) => self.numbers.push(number.as_f64().ok_or("number outside f64")?),
            Value::Bool(_) => self.booleans += 1,
            Value::Null => self.nulls += 1,
        }
        Ok(())
    }
}

/// Parse one RFC 8259 JSON text from memory with serde_json::from_slice into a
/// serde_json::Value tree. Reports the root kind, container and scalar counts,
/// container nesting depth, sorted decoded strings and numbers, and sorted
/// top-level object keys.
pub fn parse(data: &[u8]) -> Result<Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let value: Value = serde_json::from_slice(data)?;
    let root = match &value {
        Value::Object(_) => "object",
        Value::Array(_) => "array",
        Value::String(_) => "string",
        Value::Number(_) => "number",
        Value::Bool(_) => "boolean",
        Value::Null => "null",
    };
    let mut s = Summary::default();
    s.walk(&value, 0)?;
    s.numbers.sort_by(f64::total_cmp);
    s.strings.sort();
    let mut keys: Vec<&String> = value.as_object().map(|map| map.keys().collect()).unwrap_or_default();
    keys.sort();
    Ok(serde_json::json!({"root": root, "objects": s.objects, "arrays": s.arrays,
                          "booleans": s.booleans, "nulls": s.nulls, "max_depth": s.max_depth,
                          "numbers": s.numbers, "strings": s.strings, "top_level_keys": keys}))
}
