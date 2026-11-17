use std::collections::BTreeSet;
use std::error::Error;

use roxmltree::Node;

fn expanded(uri: Option<&str>, local: &str) -> String {
    match uri {
        Some(uri) if !uri.is_empty() => format!("{{{uri}}}{local}"),
        _ => local.to_string(),
    }
}

fn local_namespace_count(node: Node<'_, '_>) -> usize {
    let parent = node.parent_element();
    node.namespaces()
        .filter(|ns| {
            !parent.is_some_and(|p| {
                p.namespaces()
                    .any(|old| old.name() == ns.name() && old.uri() == ns.uri())
            })
        })
        .count()
}

/// Parse allocated UTF-8 XML into roxmltree's read-only tree. serde_json
/// encodes only the observed structure; it does not parse the input.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let doc = roxmltree::Document::parse(text)?;
    let mut elements = Vec::new();
    let mut attributes = Vec::new();
    let mut namespaces = BTreeSet::new();
    let mut text_segments = Vec::new();
    let mut declarations = 0;
    let mut max_depth = 0;
    for node in doc.descendants() {
        if node.is_element() {
            let tag = node.tag_name();
            elements.push(expanded(tag.namespace(), tag.name()));
            max_depth = max_depth.max(node.ancestors().filter(|n| n.is_element()).count());
            declarations += local_namespace_count(node);
            for ns in node.namespaces() {
                if !ns.uri().is_empty() {
                    namespaces.insert(ns.uri().to_string());
                }
            }
            for attr in node.attributes() {
                attributes.push(format!(
                    "{}={}",
                    expanded(attr.namespace(), attr.name()),
                    attr.value()
                ));
            }
        } else if node.is_text() {
            if let Some(value) = node.text() {
                let trimmed = value.trim();
                if !trimmed.is_empty() {
                    text_segments.push(trimmed.to_string());
                }
            }
        }
    }
    let root = elements.first().ok_or("missing root element")?.clone();
    Ok(
        serde_json::json!({"root": root, "elements": elements, "max_depth": max_depth,
                          "namespace_declarations": declarations, "namespaces": namespaces,
                          "attributes": attributes, "text": text_segments}),
    )
}
