use std::collections::{BTreeMap, BTreeSet};
use std::error::Error;

use xml::reader::{EventReader, XmlEvent};

#[derive(Default)]
struct Summary {
    root: Option<String>,
    elements: Vec<String>,
    max_depth: usize,
    namespace_declarations: usize,
    namespaces: BTreeSet<String>,
    attributes: Vec<String>,
    text: Vec<String>,
    pending_text: String,
    namespace_stack: Vec<BTreeMap<String, String>>,
}

fn expanded(uri: Option<&str>, local: &str) -> String {
    match uri {
        Some(uri) if !uri.is_empty() => format!("{{{uri}}}{local}"),
        _ => local.to_string(),
    }
}

impl Summary {
    fn flush(&mut self) {
        let value = self.pending_text.trim();
        if !value.is_empty() {
            self.text.push(value.to_string());
        }
        self.pending_text.clear();
    }
}

/// Pull XML 1.0 events from a local byte stream and summarize the namespace-
/// expanded structure. serde_json encodes only the observed summary.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let mut reader = EventReader::new(data);
    let mut summary = Summary::default();
    loop {
        match reader.next()? {
            XmlEvent::StartElement {
                name,
                attributes,
                namespace,
            } => {
                summary.flush();
                let element = expanded(name.namespace.as_deref(), &name.local_name);
                summary.root.get_or_insert_with(|| element.clone());
                summary.elements.push(element);
                let current: BTreeMap<String, String> = namespace
                    .iter()
                    .map(|(prefix, uri)| (prefix.to_string(), uri.to_string()))
                    .collect();
                let previous = summary.namespace_stack.last();
                for (prefix, uri) in &current {
                    if prefix == "xml" || prefix == "xmlns" {
                        continue;
                    }
                    let old = previous.and_then(|m| m.get(prefix));
                    if old != Some(uri) && !(prefix.is_empty() && uri.is_empty() && old.is_none()) {
                        summary.namespace_declarations += 1;
                    }
                    if !uri.is_empty() {
                        summary.namespaces.insert(uri.clone());
                    }
                }
                summary.namespace_stack.push(current);
                summary.max_depth = summary.max_depth.max(summary.namespace_stack.len());
                for attr in attributes {
                    summary.attributes.push(format!(
                        "{}={}",
                        expanded(attr.name.namespace.as_deref(), &attr.name.local_name),
                        attr.value
                    ));
                }
            }
            XmlEvent::EndElement { .. } => {
                summary.flush();
                summary.namespace_stack.pop().ok_or("unbalanced end tag")?;
            }
            XmlEvent::Characters(value) | XmlEvent::CData(value) | XmlEvent::Whitespace(value) => {
                summary.pending_text.push_str(&value);
            }
            XmlEvent::Comment(_) | XmlEvent::ProcessingInstruction { .. } => summary.flush(),
            XmlEvent::EndDocument => break,
            XmlEvent::StartDocument { .. } | XmlEvent::Doctype { .. } => {}
        }
    }
    summary.flush();
    if summary.root.is_none() || !summary.namespace_stack.is_empty() {
        return Err("unclosed document".into());
    }
    Ok(
        serde_json::json!({"root": summary.root, "elements": summary.elements,
                          "max_depth": summary.max_depth,
                          "namespace_declarations": summary.namespace_declarations,
                          "namespaces": summary.namespaces,
                          "attributes": summary.attributes, "text": summary.text}),
    )
}
