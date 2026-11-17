use hifijson::{
    SliceLexer,
    token::Lex,
    value::{self, Value},
};
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
    fn walk<N: AsRef<str>, S: AsRef<str>>(
        &mut self,
        value: &Value<N, S>,
        depth: u64,
    ) -> Result<(), Box<dyn Error>> {
        match value {
            Value::Object(entries) => {
                self.objects += 1;
                self.max_depth = self.max_depth.max(depth + 1);
                for (_, child) in entries {
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
            Value::String(text) => self.strings.push(text.as_ref().to_string()),
            Value::Number((number, _)) => self.numbers.push(number.as_ref().parse::<f64>()?),
            Value::Bool(_) => self.booleans += 1,
            Value::Null => self.nulls += 1,
        }
        Ok(())
    }
}

/// Parse exactly one local JSON value using hifijson's own byte-slice lexer
/// and bounded recursive value parser. serde_json encodes only the summary.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let mut lexer = SliceLexer::new(data);
    let value = lexer.exactly_one(Lex::ws_peek, |next, lexer| {
        value::parse_bounded(256, next, lexer)
    })?;
    let root = match &value {
        Value::Object(_) => "object",
        Value::Array(_) => "array",
        Value::String(_) => "string",
        Value::Number(_) => "number",
        Value::Bool(_) => "boolean",
        Value::Null => "null",
    };
    let mut summary = Summary::default();
    summary.walk(&value, 0)?;
    summary.numbers.sort_by(f64::total_cmp);
    summary.strings.sort();
    let mut keys = match &value {
        Value::Object(entries) => entries
            .iter()
            .map(|(key, _)| key.as_ref().to_string())
            .collect::<Vec<_>>(),
        _ => Vec::new(),
    };
    keys.sort();
    Ok(serde_json::json!({"root": root, "objects": summary.objects,
        "arrays": summary.arrays, "booleans": summary.booleans,
        "nulls": summary.nulls, "max_depth": summary.max_depth,
        "numbers": summary.numbers, "strings": summary.strings,
        "top_level_keys": keys}))
}
