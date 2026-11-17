use std::error::Error;

use serde_json::{Value as Json, json};
use yaml_rust2::{Yaml, YamlLoader};

/// Typed tree of controls/yaml/check_controls.py: hashes keep source order
/// (LinkedHashMap), aliases are already replaced by the loader, and Real
/// scalars are parsed with Yaml::as_f64 and printed with Rust's shortest
/// round-trip Display.
fn tagged(value: &Yaml) -> Result<Json, Box<dyn Error>> {
    Ok(match value {
        Yaml::Null => json!(["null"]),
        Yaml::Boolean(flag) => json!(["bool", flag]),
        Yaml::Integer(int) => json!(["int", int.to_string()]),
        Yaml::Real(_) => {
            let float = value.as_f64().ok_or("unparsable real")?;
            if !float.is_finite() {
                return Err("non-finite float outside the typed tree".into());
            }
            json!(["float", format!("{float}")])
        }
        Yaml::String(text) => json!(["str", text]),
        Yaml::Array(items) => {
            let nodes = items.iter().map(tagged).collect::<Result<Vec<_>, _>>()?;
            json!(["seq", nodes])
        }
        Yaml::Hash(map) => {
            let mut pairs = Vec::with_capacity(map.len());
            for (key, child) in map {
                let key = key.as_str().ok_or("non-string mapping key")?;
                pairs.push(json!([key, tagged(child)?]));
            }
            json!(["map", pairs])
        }
        Yaml::Alias(_) => return Err("unresolved alias".into()),
        Yaml::BadValue => return Err("bad value".into()),
    })
}

/// Parse YAML from local UTF-8 text with yaml_rust2::YamlLoader::load_from_str,
/// require exactly one document, and report its typed tree.
pub fn parse(data: &[u8]) -> Result<Json, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let documents = YamlLoader::load_from_str(text)?;
    if documents.len() != 1 {
        return Err(format!("expected one document, found {}", documents.len()).into());
    }
    Ok(json!({"tree": tagged(&documents[0])?}))
}
