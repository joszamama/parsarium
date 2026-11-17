use markup5ever_rcdom::{Handle, NodeData, RcDom};
use std::cell::Cell;
use std::collections::BTreeSet;
use std::error::Error;
use xml5ever::buffer_queue::BufferQueue;
use xml5ever::driver::parse_document;
use xml5ever::tendril::TendrilSink;
use xml5ever::tokenizer::{ProcessResult, Token, TokenSink, XmlTokenizer};

fn expanded(uri: &str, local: &str) -> String {
    if uri.is_empty() {
        local.to_string()
    } else {
        format!("{{{uri}}}{local}")
    }
}

#[derive(Default)]
struct Summary {
    elements: Vec<String>,
    max_depth: usize,
    namespaces: BTreeSet<String>,
    attributes: Vec<String>,
    text: Vec<String>,
}

fn visit(node: &Handle, depth: usize, s: &mut Summary) {
    let mut child_depth = depth;
    match &node.data {
        NodeData::Element { name, attrs, .. } => {
            child_depth += 1;
            s.max_depth = s.max_depth.max(child_depth);
            s.elements.push(expanded(&name.ns, &name.local));
            if !name.ns.is_empty() {
                s.namespaces.insert(name.ns.to_string());
            }
            for attr in attrs.borrow().iter() {
                s.attributes.push(format!(
                    "{}={}",
                    expanded(&attr.name.ns, &attr.name.local),
                    attr.value
                ));
            }
        }
        NodeData::Text { contents } => {
            let value = contents.borrow();
            let trimmed = value.trim();
            if !trimmed.is_empty() {
                s.text.push(trimmed.to_string());
            }
        }
        _ => {}
    }
    for child in node.children.borrow().iter() {
        visit(child, child_depth, s);
    }
}

#[derive(Default)]
struct DeclarationCounter(Cell<usize>);
impl TokenSink for DeclarationCounter {
    type Handle = ();
    fn process_token(&self, token: Token) -> ProcessResult<()> {
        if let Token::Tag(tag) = token {
            let n = tag
                .attrs
                .iter()
                .filter(|attr| {
                    attr.name
                        .prefix
                        .as_ref()
                        .is_some_and(|prefix| &**prefix == "xmlns")
                        || &*attr.name.local == "xmlns"
                })
                .count();
            self.0.set(self.0.get() + n);
        }
        ProcessResult::Continue
    }
}

fn count_namespace_declarations(text: &str) -> usize {
    let queue = BufferQueue::default();
    queue.push_back(text.into());
    let tok = XmlTokenizer::new(DeclarationCounter::default(), Default::default());
    let _ = tok.feed(&queue);
    tok.end();
    tok.sink.0.get()
}

/// The XML5 tree builder resolves names; its tokenizer separately counts
/// namespace declarations that the tree builder removes from DOM attributes.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let dom = parse_document(RcDom::default(), Default::default()).one(text);
    let mut s = Summary::default();
    visit(&dom.document, 0, &mut s);
    let root = s.elements.first().ok_or("missing root element")?.clone();
    Ok(serde_json::json!({"root": root, "elements": s.elements,
      "max_depth": s.max_depth,
      "namespace_declarations": count_namespace_declarations(text),
      "namespaces": s.namespaces,
      "attributes": s.attributes, "text": s.text}))
}
