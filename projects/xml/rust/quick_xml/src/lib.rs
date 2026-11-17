use std::collections::BTreeSet;
use std::error::Error;

use quick_xml::NsReader;
use quick_xml::XmlVersion;
use quick_xml::escape::resolve_predefined_entity;
use quick_xml::events::{BytesStart, Event};
use quick_xml::name::{NamespaceResolver, ResolveResult};

#[derive(Default)]
struct Summary {
    root: Option<String>,
    elements: Vec<String>,
    depth: u64,
    max_depth: u64,
    declarations: u64,
    namespaces: BTreeSet<String>,
    attributes: Vec<String>,
    text: String,
    segments: Vec<String>,
}

fn expanded(resolved: ResolveResult<'_>, local: &str) -> Result<String, Box<dyn Error>> {
    match resolved {
        ResolveResult::Bound(ns) => Ok(format!("{{{}}}{}", ns.as_ref(), local)),
        ResolveResult::Unbound => Ok(local.to_string()),
        ResolveResult::Unknown(prefix) => Err(format!("unbound prefix {prefix}").into()),
    }
}

impl Summary {
    fn flush(&mut self) {
        let trimmed = self.text.trim();
        if !trimmed.is_empty() {
            self.segments.push(trimmed.to_string());
        }
        self.text.clear();
    }

    fn open(&mut self, resolver: &NamespaceResolver, start: &BytesStart<'_>) -> Result<(), Box<dyn Error>> {
        self.flush();
        let (resolved, local) = resolver.resolve_element(start.name());
        let name = expanded(resolved, local.as_ref())?;
        self.root.get_or_insert_with(|| name.clone());
        self.elements.push(name);
        self.max_depth = self.max_depth.max(self.depth + 1);
        for attr in start.attributes() {
            let attr = attr?;
            let value = attr.normalized_value(XmlVersion::Implicit1_0)?;
            if attr.key.as_namespace_binding().is_some() {
                self.declarations += 1;
                if !value.is_empty() {
                    self.namespaces.insert(value.into_owned());
                }
                continue;
            }
            let (resolved, local) = resolver.resolve_attribute(attr.key);
            self.attributes.push(format!("{}={}", expanded(resolved, local.as_ref())?, value));
        }
        Ok(())
    }
}

/// Read an XML 1.0 document from memory with namespace resolution. Reports the
/// root and element expanded names, attributes, namespace declarations, and
/// decoded character data (entity and character references, CDATA).
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let mut reader = NsReader::from_reader(data);
    reader.config_mut().check_end_names = true;
    let mut s = Summary::default();
    loop {
        match reader.read_event()? {
            Event::Start(start) => {
                s.open(reader.resolver(), &start)?;
                s.depth += 1;
            }
            Event::Empty(start) => s.open(reader.resolver(), &start)?,
            Event::End(_) => {
                s.flush();
                s.depth = s.depth.checked_sub(1).ok_or("unbalanced end tag")?;
            }
            Event::Text(t) => s.text.push_str(&t.xml10_content()),
            Event::CData(t) => s.text.push_str(&t.xml10_content()),
            Event::GeneralRef(r) => match r.resolve_char_ref()? {
                Some(ch) => s.text.push(ch),
                None => s.text.push_str(resolve_predefined_entity(&r.xml10_content()).ok_or("undeclared entity")?),
            },
            Event::Comment(_) | Event::PI(_) => s.flush(),
            Event::Decl(_) | Event::DocType(_) => {}
            Event::Eof => break,
        }
    }
    if s.depth != 0 || s.root.is_none() {
        return Err("document element not closed".into());
    }
    Ok(serde_json::json!({"root": s.root, "elements": s.elements, "max_depth": s.max_depth,
                          "namespace_declarations": s.declarations, "namespaces": s.namespaces,
                          "attributes": s.attributes, "text": s.segments}))
}
