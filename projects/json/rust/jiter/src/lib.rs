use std::error::Error;

use jiter::JsonValue;

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
    fn walk(&mut self, value: &JsonValue<'_>, depth: u64) -> Result<(), Box<dyn Error>> {
        match value {
            JsonValue::Object(items) => {
                self.objects += 1;
                self.max_depth = self.max_depth.max(depth + 1);
                for (_, child) in items.iter() {
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
            JsonValue::Str(text) => self.strings.push(text.to_string()),
            JsonValue::Bool(_) => self.booleans += 1,
            JsonValue::Null => self.nulls += 1,
            JsonValue::Int(number) => self.numbers.push(*number as f64),
            JsonValue::BigInt(number) => self.numbers.push(number.to_string().parse()?),
            JsonValue::Float(number) => self.numbers.push(*number),
        }
        Ok(())
    }
}

/// Parse local JSON bytes with Jiter's own JsonValue parser in strict mode.
/// serde_json encodes only the observed summary.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let value = JsonValue::parse(data, false)?;
    let root = match &value {
        JsonValue::Object(_) => "object",
        JsonValue::Array(_) => "array",
        JsonValue::Str(_) => "string",
        JsonValue::Int(_) | JsonValue::BigInt(_) | JsonValue::Float(_) => "number",
        JsonValue::Bool(_) => "boolean",
        JsonValue::Null => "null",
    };
    let mut summary = Summary::default();
    summary.walk(&value, 0)?;
    summary.numbers.sort_by(f64::total_cmp);
    summary.strings.sort();
    let mut keys: Vec<String> = match &value {
        JsonValue::Object(items) => items.iter().map(|(key, _)| key.to_string()).collect(),
        _ => Vec::new(),
    };
    keys.sort();
    Ok(serde_json::json!({"root": root, "objects": summary.objects,
                          "arrays": summary.arrays, "booleans": summary.booleans,
                          "nulls": summary.nulls, "max_depth": summary.max_depth,
                          "numbers": summary.numbers, "strings": summary.strings,
                          "top_level_keys": keys}))
}
