use std::error::Error;

use parsarium_yaml_saphyr_events::{Scalar, Yaml};
use serde_json::{Value as Json, json};

/// Typed tree of controls/yaml/check_controls.py: saphyr's loader resolves plain
/// scalars (early_parse, the default) into Scalar values, copies anchored nodes
/// for aliases, and keeps mappings in source order (hashlink LinkedHashMap).
/// Floats are printed with Rust's shortest round-trip Display.
fn tagged(value: &Yaml) -> Result<Json, Box<dyn Error>> {
    Ok(match value {
        Yaml::Value(Scalar::Null) => json!(["null"]),
        Yaml::Value(Scalar::Boolean(flag)) => json!(["bool", flag]),
        Yaml::Value(Scalar::Integer(int)) => json!(["int", int.to_string()]),
        Yaml::Value(Scalar::FloatingPoint(float)) => {
            let float = float.into_inner();
            if !float.is_finite() {
                return Err("non-finite float outside the typed tree".into());
            }
            json!(["float", format!("{float}")])
        }
        Yaml::Value(Scalar::String(text)) => json!(["str", text]),
        Yaml::Sequence(items) => {
            let nodes = items.iter().map(tagged).collect::<Result<Vec<_>, _>>()?;
            json!(["seq", nodes])
        }
        Yaml::Mapping(map) => {
            let mut pairs = Vec::with_capacity(map.len());
            for (key, child) in map {
                let Yaml::Value(Scalar::String(key)) = key else {
                    return Err("non-string mapping key".into());
                };
                pairs.push(json!([key, tagged(child)?]));
            }
            json!(["map", pairs])
        }
        Yaml::Representation(..) => return Err("unresolved scalar representation".into()),
        Yaml::Tagged(..) => return Err("explicit tag outside the controls' scope".into()),
        Yaml::Alias(_) => return Err("unresolved alias".into()),
        Yaml::BadValue => return Err("bad value".into()),
    })
}

/// Parse YAML from local UTF-8 text with saphyr's Yaml::load_from_str
/// (LoadableYamlNode), require exactly one document, and report its typed tree.
pub fn parse(data: &[u8]) -> Result<Json, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let documents = parsarium_yaml_saphyr_events::load(text)?;
    if documents.len() != 1 {
        return Err(format!("expected one document, found {}", documents.len()).into());
    }
    Ok(json!({"tree": tagged(&documents[0])?}))
}
