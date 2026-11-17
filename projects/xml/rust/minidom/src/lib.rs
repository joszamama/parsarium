use std::collections::BTreeSet;
use std::error::Error;

use minidom::{Element, Node};

fn expanded(uri: &str, local: &str) -> String {
    if uri.is_empty() {
        local.to_string()
    } else {
        format!("{{{uri}}}{local}")
    }
}

#[derive(Default)]
struct Summary {
    attributes: Vec<String>,
    elements: Vec<String>,
    max_depth: usize,
    namespace_declarations: usize,
    namespaces: BTreeSet<String>,
    text: Vec<String>,
    pending_text: String,
}

impl Summary {
    fn flush_text(&mut self) {
        let segment = self.pending_text.trim();
        if !segment.is_empty() {
            self.text.push(segment.to_string());
        }
        self.pending_text.clear();
    }

    fn walk(&mut self, element: &Element, depth: usize) {
        self.flush_text();
        self.max_depth = self.max_depth.max(depth);
        self.elements.push(expanded(&element.ns(), element.name()));
        // minidom keeps each element's xmlns declarations in Element::prefixes.
        for namespace in element.prefixes.declared_prefixes().values() {
            self.namespace_declarations += 1;
            if !namespace.is_empty() {
                self.namespaces.insert(namespace.to_string());
            }
        }
        // AttrMap (from rxml) iterates by (namespace URI, local name).
        for ((namespace, local), value) in element.attrs().iter() {
            self.attributes.push(format!("{}={}", expanded(namespace, local), value));
        }
        for node in element.nodes() {
            match node {
                Node::Element(child) => self.walk(child, depth + 1),
                Node::Text(value) => self.pending_text.push_str(value),
            }
        }
        self.flush_text();
    }
}

/// Parse one local XML byte buffer with minidom's documented
/// `Element::from_reader(BufRead)` API, which drives rxml's RawReader into
/// minidom's own TreeBuilder (prefix resolution and DOM).
/// serde_json only encodes the observed DOM summary; it does not parse input.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let root = Element::from_reader(data)?;
    let mut summary = Summary::default();
    summary.walk(&root, 1);
    Ok(serde_json::json!({
        "root": summary.elements[0],
        "elements": summary.elements,
        "max_depth": summary.max_depth,
        "namespace_declarations": summary.namespace_declarations,
        "namespaces": summary.namespaces,
        "attributes": summary.attributes,
        "text": summary.text,
    }))
}
