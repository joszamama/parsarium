use std::error::Error;
use std::fmt;

use serde::de::{Deserialize, Deserializer, MapAccess, SeqAccess, Visitor};
use serde_json::{Value as Json, json};

/// Typed tree of controls/yaml/check_controls.py, built by a Deserialize visitor
/// over serde-saphyr's self-describing deserialize_any: maps keep source order,
/// integers and floats keep the type serde-saphyr resolved, quoted scalars stay
/// strings, and aliases are replayed by serde-saphyr.
struct Node(Json);

impl<'de> Deserialize<'de> for Node {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        deserializer.deserialize_any(NodeVisitor)
    }
}

struct NodeVisitor;

impl<'de> Visitor<'de> for NodeVisitor {
    type Value = Node;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a YAML node")
    }

    fn visit_unit<E>(self) -> Result<Node, E> {
        Ok(Node(json!(["null"])))
    }

    fn visit_none<E>(self) -> Result<Node, E> {
        Ok(Node(json!(["null"])))
    }

    fn visit_some<D: Deserializer<'de>>(self, deserializer: D) -> Result<Node, D::Error> {
        Node::deserialize(deserializer)
    }

    fn visit_bool<E>(self, flag: bool) -> Result<Node, E> {
        Ok(Node(json!(["bool", flag])))
    }

    fn visit_i64<E>(self, int: i64) -> Result<Node, E> {
        Ok(Node(json!(["int", int.to_string()])))
    }

    fn visit_u64<E>(self, int: u64) -> Result<Node, E> {
        Ok(Node(json!(["int", int.to_string()])))
    }

    fn visit_i128<E>(self, int: i128) -> Result<Node, E> {
        Ok(Node(json!(["int", int.to_string()])))
    }

    fn visit_u128<E>(self, int: u128) -> Result<Node, E> {
        Ok(Node(json!(["int", int.to_string()])))
    }

    fn visit_f64<E: serde::de::Error>(self, float: f64) -> Result<Node, E> {
        if !float.is_finite() {
            return Err(E::custom("non-finite float outside the typed tree"));
        }
        Ok(Node(json!(["float", format!("{float}")])))
    }

    fn visit_str<E>(self, text: &str) -> Result<Node, E> {
        Ok(Node(json!(["str", text])))
    }

    fn visit_seq<A: SeqAccess<'de>>(self, mut seq: A) -> Result<Node, A::Error> {
        let mut items = Vec::new();
        while let Some(Node(item)) = seq.next_element()? {
            items.push(item);
        }
        Ok(Node(json!(["seq", items])))
    }

    fn visit_map<A: MapAccess<'de>>(self, mut map: A) -> Result<Node, A::Error> {
        let mut pairs = Vec::new();
        while let Some(key) = map.next_key::<String>()? {
            let Node(value) = map.next_value()?;
            pairs.push(json!([key, value]));
        }
        Ok(Node(json!(["map", pairs])))
    }
}

/// Parse one YAML document from local UTF-8 text with serde_saphyr::from_str
/// into the harness's order-keeping Deserialize type and report its typed tree.
pub fn parse(data: &[u8]) -> Result<Json, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let Node(tree) = serde_saphyr::from_str(text)?;
    Ok(json!({"tree": tree}))
}
