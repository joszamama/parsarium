use std::collections::BTreeSet;
use std::error::Error;

use uppsala::dom::{Document, NodeId, NodeKind};

fn expanded(uri: Option<&str>, local: &str) -> String {
    match uri {
        Some(uri) if !uri.is_empty() => format!("{{{uri}}}{local}"),
        _ => local.to_string(),
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

    fn walk(&mut self, doc: &Document<'_>, id: NodeId, depth: usize) {
        match doc.node_kind(id) {
            Some(NodeKind::Element(element)) => {
                self.flush_text();
                self.max_depth = self.max_depth.max(depth + 1);
                self.elements.push(expanded(element.name.namespace_uri.as_deref(),
                                            &element.name.local_name));
                self.namespace_declarations += element.namespace_declarations.len();
                for (_, uri) in &element.namespace_declarations {
                    if !uri.is_empty() {
                        self.namespaces.insert(uri.to_string());
                    }
                }
                for attribute in &element.attributes {
                    self.attributes.push(format!("{}={}",
                        expanded(attribute.name.namespace_uri.as_deref(),
                                 &attribute.name.local_name), attribute.value));
                }
                for child in doc.children_iter(id) {
                    self.walk(doc, child, depth + 1);
                }
                self.flush_text();
            }
            Some(NodeKind::Text(value) | NodeKind::CData(value)) => {
                self.pending_text.push_str(value);
            }
            Some(NodeKind::Document) => {
                for child in doc.children_iter(id) {
                    self.walk(doc, child, depth);
                }
                self.flush_text();
            }
            Some(NodeKind::Comment(_) | NodeKind::ProcessingInstruction(_)) => self.flush_text(),
            Some(NodeKind::Attribute(_, _)) | None => {}
        }
    }
}

/// Parse one local XML byte buffer with uppsala's documented parse_bytes API.
/// serde_json only encodes the observed DOM summary; it does not parse input.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let doc = uppsala::parse_bytes(data)?;
    let mut summary = Summary::default();
    summary.walk(&doc, doc.root(), 0);
    let root = summary.elements.first().ok_or("missing document element")?.clone();
    Ok(serde_json::json!({
        "root": root,
        "elements": summary.elements,
        "max_depth": summary.max_depth,
        "namespace_declarations": summary.namespace_declarations,
        "namespaces": summary.namespaces,
        "attributes": summary.attributes,
        "text": summary.text,
    }))
}
