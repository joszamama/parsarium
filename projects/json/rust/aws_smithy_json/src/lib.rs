use std::error::Error;

use aws_smithy_json::deserialize::{Token, json_token_iter};
use aws_smithy_types::Number;

#[derive(Clone, Copy, PartialEq)]
enum Container {
    Object,
    Array,
}

#[derive(Default)]
struct Summary {
    root: Option<&'static str>,
    stack: Vec<Container>,
    complete: bool,
    objects: u64,
    arrays: u64,
    booleans: u64,
    nulls: u64,
    max_depth: u64,
    numbers: Vec<f64>,
    strings: Vec<String>,
    top_level_keys: Vec<String>,
}

impl Summary {
    fn begin_value(&mut self, root: &'static str) -> Result<(), Box<dyn Error>> {
        if self.complete {
            return Err("more than one JSON root value".into());
        }
        if self.root.is_none() {
            self.root = Some(root);
        }
        Ok(())
    }

    fn finish_scalar(&mut self) {
        if self.stack.is_empty() {
            self.complete = true;
        }
    }

    fn open(&mut self, kind: Container) {
        self.stack.push(kind);
        self.max_depth = self.max_depth.max(self.stack.len() as u64);
    }

    fn close(&mut self, kind: Container) -> Result<(), Box<dyn Error>> {
        if self.stack.pop() != Some(kind) {
            return Err("unbalanced JSON container".into());
        }
        if self.stack.is_empty() {
            self.complete = true;
        }
        Ok(())
    }
}

/// Consume the public AWS Smithy JSON token iterator over local bytes and
/// report decoded structure. The adapter requires one balanced root value;
/// serde_json encodes only the summary and never parses the input.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let mut s = Summary::default();
    for token in json_token_iter(data) {
        match token? {
            Token::StartObject { .. } => {
                s.begin_value("object")?;
                s.objects += 1;
                s.open(Container::Object);
            }
            Token::EndObject { .. } => s.close(Container::Object)?,
            Token::StartArray { .. } => {
                s.begin_value("array")?;
                s.arrays += 1;
                s.open(Container::Array);
            }
            Token::EndArray { .. } => s.close(Container::Array)?,
            Token::ObjectKey { key, .. } => {
                if s.stack.last() != Some(&Container::Object) {
                    return Err("object key outside object".into());
                }
                if s.stack.len() == 1 {
                    s.top_level_keys.push(key.to_unescaped()?.into_owned());
                } else {
                    let _ = key.to_unescaped()?;
                }
            }
            Token::ValueBool { .. } => {
                s.begin_value("boolean")?;
                s.booleans += 1;
                s.finish_scalar();
            }
            Token::ValueNull { .. } => {
                s.begin_value("null")?;
                s.nulls += 1;
                s.finish_scalar();
            }
            Token::ValueNumber { value, .. } => {
                s.begin_value("number")?;
                s.numbers.push(match value {
                    Number::PosInt(n) => n as f64,
                    Number::NegInt(n) => n as f64,
                    Number::Float(n) => n,
                });
                s.finish_scalar();
            }
            Token::ValueString { value, .. } => {
                s.begin_value("string")?;
                s.strings.push(value.to_unescaped()?.into_owned());
                s.finish_scalar();
            }
        }
    }
    if !s.complete || !s.stack.is_empty() {
        return Err("incomplete JSON document".into());
    }
    s.numbers.sort_by(f64::total_cmp);
    s.strings.sort();
    s.top_level_keys.sort();
    Ok(serde_json::json!({"root": s.root, "objects": s.objects,
                          "arrays": s.arrays, "booleans": s.booleans,
                          "nulls": s.nulls, "max_depth": s.max_depth,
                          "numbers": s.numbers, "strings": s.strings,
                          "top_level_keys": s.top_level_keys}))
}
