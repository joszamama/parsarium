use std::error::Error;

use noyalib::{Number, Value};
use serde_json::{Value as Json, json};

/// Typed tree of controls/yaml/check_controls.py: noyalib's Mapping is an
/// IndexMap (source order), aliases are expanded by noyalib's loader, and
/// floats use Rust's shortest round-trip Display.
fn tagged(value: &Value) -> Result<Json, Box<dyn Error>> {
    Ok(match value {
        Value::Null => json!(["null"]),
        Value::Bool(flag) => json!(["bool", flag]),
        Value::Number(Number::Integer(int)) => json!(["int", int.to_string()]),
        Value::Number(Number::Float(float)) => {
            if !float.is_finite() {
                return Err("non-finite float outside the typed tree".into());
            }
            json!(["float", format!("{float}")])
        }
        #[allow(unreachable_patterns)]
        Value::Number(_) => return Err("number outside the typed tree".into()),
        Value::String(text) => json!(["str", text]),
        Value::Sequence(items) => {
            let nodes = items.iter().map(tagged).collect::<Result<Vec<_>, _>>()?;
            json!(["seq", nodes])
        }
        Value::Mapping(map) => {
            let mut pairs = Vec::with_capacity(map.len());
            for (key, child) in map.iter() {
                pairs.push(json!([key, tagged(child)?]));
            }
            json!(["map", pairs])
        }
        Value::Tagged(_) => return Err("explicit tag outside the controls' scope".into()),
    })
}

/// Parse one YAML document from local UTF-8 text with
/// noyalib::from_str::<noyalib::Value> and report its typed tree.
pub fn parse(data: &[u8]) -> Result<Json, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let value: Value = noyalib::from_str(text)?;
    Ok(json!({"tree": tagged(&value)?}))
}
