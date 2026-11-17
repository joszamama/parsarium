use std::collections::BTreeSet;
use std::error::Error;

use instant_xml::AnyElement;

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
    namespaces: BTreeSet<String>,
    text: Vec<String>,
}

impl Summary {
    fn walk(&mut self, element: &AnyElement<'_>, depth: usize) {
        self.max_depth = self.max_depth.max(depth);
        self.elements.push(expanded(&element.ns, &element.name));
        if !element.ns.is_empty() {
            self.namespaces.insert(element.ns.to_string());
        }
        // instant-xml consumes xmlns declarations to resolve prefixes; only
        // ordinary attributes, in document order, reach AnyElement.
        for attribute in &element.attributes {
            if !attribute.ns.is_empty() {
                self.namespaces.insert(attribute.ns.to_string());
            }
            self.attributes
                .push(format!("{}={}", expanded(&attribute.ns, &attribute.name), attribute.value));
        }
        for child in &element.children {
            self.walk(child, depth + 1);
        }
        // AnyElement keeps one text value per element: the last text node
        // (decoded character data or CDATA) before its end tag.
        if let Some(text) = &element.text {
            let segment = text.trim();
            if !segment.is_empty() {
                self.text.push(segment.to_string());
            }
        }
    }
}

/// Parse one local XML buffer with instant-xml's documented
/// `from_str::<AnyElement>(&str)` API. instant-xml drives the xmlparser
/// tokenizer and resolves namespaces, decodes references and builds the
/// AnyElement tree itself. The bytes are decoded as UTF-8 locally first.
/// serde_json only encodes the observed tree summary; it does not parse input.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let root: AnyElement<'_> = instant_xml::from_str(text)?;
    let mut summary = Summary::default();
    summary.walk(&root, 1);
    Ok(serde_json::json!({
        "root": summary.elements[0],
        "elements": summary.elements,
        "max_depth": summary.max_depth,
        "namespaces": summary.namespaces,
        "attributes": summary.attributes,
        "text": summary.text,
    }))
}
