use std::error::Error;

use sonic_rs::prelude::JsonNumberTrait;
use sonic_rs::{Value, ValueRef};

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
        match value.as_ref() {
            ValueRef::Object(map) => {
                self.objects += 1;
                self.max_depth = self.max_depth.max(depth + 1);
                for (_, child) in map.iter() {
                    self.walk(child, depth + 1)?;
                }
            }
            ValueRef::Array(items) => {
                self.arrays += 1;
                self.max_depth = self.max_depth.max(depth + 1);
                for child in items.iter() {
                    self.walk(child, depth + 1)?;
                }
            }
            ValueRef::String(text) => self.strings.push(text.to_string()),
            ValueRef::Bool(_) => self.booleans += 1,
            ValueRef::Null => self.nulls += 1,
            ValueRef::Number(number) => self.numbers.push(number.as_f64().ok_or("non-f64 number")?),
        }
        Ok(())
    }
}

/// Parse local JSON bytes into sonic-rs's own untyped DOM, then summarize it.
/// serde_json only encodes the observed summary.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let value: Value = sonic_rs::from_slice(data)?;
    let root = match value.as_ref() {
        ValueRef::Object(_) => "object",
        ValueRef::Array(_) => "array",
        ValueRef::String(_) => "string",
        ValueRef::Number(_) => "number",
        ValueRef::Bool(_) => "boolean",
        ValueRef::Null => "null",
    };
    let mut summary = Summary::default();
    summary.walk(&value, 0)?;
    summary.numbers.sort_by(f64::total_cmp);
    summary.strings.sort();
    let mut keys: Vec<String> = match value.as_ref() {
        ValueRef::Object(map) => map.iter().map(|(key, _)| key.to_string()).collect(),
        _ => Vec::new(),
    };
    keys.sort();
    Ok(serde_json::json!({"root": root, "objects": summary.objects,
                          "arrays": summary.arrays, "booleans": summary.booleans,
                          "nulls": summary.nulls, "max_depth": summary.max_depth,
                          "numbers": summary.numbers, "strings": summary.strings,
                          "top_level_keys": keys}))
}
