use std::collections::BTreeSet;
use std::error::Error;

use xml::{Event, Parser};

const XMLNS_URI: &str = "http://www.w3.org/2000/xmlns/";

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
    depth: usize,
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
}

/// Parse one local UTF-8 XML buffer with RustyXML's documented
/// `Parser::new()` / `feed_str(&str)` event API. RustyXML resolves element
/// and attribute namespaces itself; `StartTag.attributes` is a HashMap, so the
/// adapter lists each element's attributes sorted by (namespace, local name).
/// serde_json only encodes the observed summary; it does not parse input.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let mut parser = Parser::new();
    parser.feed_str(text);
    let mut summary = Summary::default();
    for event in parser {
        match event? {
            Event::ElementStart(tag) => {
                summary.flush_text();
                summary.depth += 1;
                summary.max_depth = summary.max_depth.max(summary.depth);
                summary.elements.push(expanded(tag.ns.as_deref(), &tag.name));
                let mut attributes: Vec<_> = tag.attributes.into_iter().collect();
                attributes.sort_by(|((a_name, a_ns), _), ((b_name, b_ns), _)| (a_ns, a_name).cmp(&(b_ns, b_name)));
                for ((name, ns), value) in attributes {
                    let declaration = match ns.as_deref() {
                        None => name == "xmlns",
                        Some(uri) => uri == XMLNS_URI,
                    };
                    if declaration {
                        summary.namespace_declarations += 1;
                        if !value.is_empty() {
                            summary.namespaces.insert(value);
                        }
                    } else {
                        summary.attributes.push(format!("{}={}", expanded(ns.as_deref(), &name), value));
                    }
                }
            }
            Event::ElementEnd(_) => {
                summary.flush_text();
                summary.depth = summary.depth.checked_sub(1).ok_or("unbalanced end tag")?;
            }
            Event::Characters(value) | Event::CDATA(value) => summary.pending_text.push_str(&value),
            Event::Comment(_) | Event::PI(_) => summary.flush_text(),
        }
    }
    summary.flush_text();
    if summary.depth != 0 {
        return Err("unclosed element".into());
    }
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
