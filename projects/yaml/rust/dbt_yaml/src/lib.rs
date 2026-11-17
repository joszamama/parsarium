use std::error::Error;

use dbt_yaml::Value;
use serde_json::{Value as Json, json};

/// Typed tree of controls/yaml/check_controls.py: dbt-yaml's spanned Value keeps
/// mappings in source order, aliases are expanded by its loader, and floats use
/// Rust's shortest round-trip Display. Source spans are ignored.
fn tagged(value: &Value) -> Result<Json, Box<dyn Error>> {
    Ok(match value {
        Value::Null(..) => json!(["null"]),
        Value::Bool(flag, _) => json!(["bool", flag]),
        Value::Number(number, _) => {
            if let Some(int) = number.as_i64() {
                json!(["int", int.to_string()])
            } else if let Some(int) = number.as_u64() {
                json!(["int", int.to_string()])
            } else {
                let float = number.as_f64().ok_or("number outside f64")?;
                if !float.is_finite() {
                    return Err("non-finite float outside the typed tree".into());
                }
                json!(["float", format!("{float}")])
            }
        }
        Value::String(text, _) => json!(["str", text]),
        Value::Sequence(items, _) => {
            let nodes = items.iter().map(tagged).collect::<Result<Vec<_>, _>>()?;
            json!(["seq", nodes])
        }
        Value::Mapping(map, _) => {
            let mut pairs = Vec::with_capacity(map.len());
            for (key, child) in map {
                let key = key.as_str().ok_or("non-string mapping key")?;
                pairs.push(json!([key, tagged(child)?]));
            }
            json!(["map", pairs])
        }
        Value::Tagged(..) => return Err("explicit tag outside the controls' scope".into()),
    })
}

/// Parse one YAML document from local UTF-8 text with
/// dbt_yaml::from_str::<dbt_yaml::Value> and report its typed tree.
pub fn parse(data: &[u8]) -> Result<Json, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let value: Value = dbt_yaml::from_str(text)?;
    Ok(json!({"tree": tagged(&value)?}))
}
