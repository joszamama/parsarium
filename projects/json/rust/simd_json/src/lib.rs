use std::error::Error;

use simd_json::{OwnedValue as Value, StaticNode};

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
                for child in items.iter() {
                    self.walk(child, depth + 1)?;
                }
            }
            Value::String(text) => self.strings.push(text.clone()),
            Value::Static(StaticNode::Bool(_)) => self.booleans += 1,
            Value::Static(StaticNode::Null) => self.nulls += 1,
            Value::Static(StaticNode::I64(number)) => self.numbers.push(*number as f64),
            Value::Static(StaticNode::U64(number)) => self.numbers.push(*number as f64),
            Value::Static(StaticNode::F64(number)) => self.numbers.push(*number),
        }
        Ok(())
    }
}

/// Parse a local mutable byte buffer into simd-json's own untyped DOM, then
/// summarize structure. serde_json is used only to encode the summary.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let mut buffer = data.to_vec();
    let value = simd_json::to_owned_value(&mut buffer)?;
    let root = match &value {
        Value::Object(_) => "object",
        Value::Array(_) => "array",
        Value::String(_) => "string",
        Value::Static(StaticNode::Bool(_)) => "boolean",
        Value::Static(StaticNode::Null) => "null",
        Value::Static(_) => "number",
    };
    let mut s = Summary::default();
    s.walk(&value, 0)?;
    s.numbers.sort_by(f64::total_cmp);
    s.strings.sort();
    let mut keys: Vec<&String> = match &value {
        Value::Object(map) => map.keys().collect(),
        _ => Vec::new(),
    };
    keys.sort();
    Ok(
        serde_json::json!({"root": root, "objects": s.objects, "arrays": s.arrays,
                          "booleans": s.booleans, "nulls": s.nulls, "max_depth": s.max_depth,
                          "numbers": s.numbers, "strings": s.strings, "top_level_keys": keys}),
    )
}
