use miniserde::json::{Number, Value};
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
}

impl Summary {
    fn walk(&mut self, root: &Value) {
        let mut pending = vec![(root, 0_u64)];
        while let Some((value, depth)) = pending.pop() {
            match value {
                Value::Object(map) => {
                    self.objects += 1;
                    self.max_depth = self.max_depth.max(depth + 1);
                    pending.extend(map.values().map(|child| (child, depth + 1)));
                }
                Value::Array(items) => {
                    self.arrays += 1;
                    self.max_depth = self.max_depth.max(depth + 1);
                    pending.extend(items.iter().map(|child| (child, depth + 1)));
                }
                Value::String(text) => self.strings.push(text.clone()),
                Value::Number(number) => self.numbers.push(match number {
                    Number::U64(n) => *n as f64,
                    Number::I64(n) => *n as f64,
                    Number::F64(n) => *n,
                }),
                Value::Bool(_) => self.booleans += 1,
                Value::Null => self.nulls += 1,
            }
        }
    }
}

/// Decode one local UTF-8 JSON text into miniserde's own generic Value tree.
/// The walk is iterative, matching the parser's non-recursive design.
/// serde_json encodes the observed summary only.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let value: Value = miniserde::json::from_str(text)?;
    let root = match &value {
        Value::Object(_) => "object",
        Value::Array(_) => "array",
        Value::String(_) => "string",
        Value::Number(_) => "number",
        Value::Bool(_) => "boolean",
        Value::Null => "null",
    };
    let mut summary = Summary::default();
    summary.walk(&value);
    summary.numbers.sort_by(f64::total_cmp);
    summary.strings.sort();
    let mut keys = match &value {
        Value::Object(map) => map.keys().cloned().collect::<Vec<_>>(),
        _ => Vec::new(),
    };
    keys.sort();
    Ok(serde_json::json!({"root": root, "objects": summary.objects,
        "arrays": summary.arrays, "booleans": summary.booleans,
        "nulls": summary.nulls, "max_depth": summary.max_depth,
        "numbers": summary.numbers, "strings": summary.strings,
        "top_level_keys": keys}))
}
