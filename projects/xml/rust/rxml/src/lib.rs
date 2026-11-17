use rxml::{Event, Parse, Parser, RawEvent, RawParser};
use std::collections::BTreeSet;
use std::error::Error;

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
    depth: usize,
    max_depth: usize,
    namespaces: BTreeSet<String>,
    attributes: Vec<String>,
    pending: String,
    text: Vec<String>,
}

impl Summary {
    fn flush(&mut self) {
        let trimmed = self.pending.trim();
        if !trimmed.is_empty() {
            self.text.push(trimmed.to_string());
        }
        self.pending.clear();
    }

    fn event(&mut self, event: Event) {
        match event {
            Event::StartElement(_, (ns, local), attrs) => {
                self.flush();
                self.depth += 1;
                self.max_depth = self.max_depth.max(self.depth);
                self.elements.push(expanded(&ns, &local));
                if !ns.is_empty() {
                    self.namespaces.insert(ns.to_string());
                }
                // AttrMap iterates by (namespace URI, local name).
                for ((ns, local), value) in attrs.iter() {
                    self.attributes.push(format!("{}={}", expanded(ns, local), value));
                }
            }
            Event::EndElement(_) => {
                self.flush();
                self.depth -= 1;
            }
            Event::Text(_, text) => self.pending.push_str(&text),
            Event::XmlDeclaration(..) => {}
        }
    }
}

/// The namespace resolver drops xmlns attributes, so rxml's own raw parser
/// counts the declarations in a second pass.
fn count_namespace_declarations(data: &[u8]) -> Result<usize, Box<dyn Error>> {
    let mut parser = RawParser::new();
    let mut count = 0;
    parser
        .parse_all(&mut &data[..], true, |event| {
            if let RawEvent::Attribute(_, (prefix, local), _) = event {
                if prefix.as_deref().is_some_and(|p| p == "xmlns")
                    || (prefix.is_none() && local == "xmlns")
                {
                    count += 1;
                }
            }
        })
        .map_err(|err| format!("{err:?}"))?;
    Ok(count)
}

pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let mut parser = Parser::new();
    let mut s = Summary::default();
    parser
        .parse_all(&mut &data[..], true, |event| s.event(event))
        .map_err(|err| format!("{err:?}"))?;
    let root = s.elements.first().ok_or("missing root element")?.clone();
    Ok(serde_json::json!({"root": root, "elements": s.elements,
      "max_depth": s.max_depth,
      "namespace_declarations": count_namespace_declarations(data)?,
      "namespaces": s.namespaces,
      "attributes": s.attributes, "text": s.text}))
}
