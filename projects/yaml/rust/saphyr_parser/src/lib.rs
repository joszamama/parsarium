use std::collections::BTreeMap;
use std::error::Error;

use parsarium_yaml_saphyr_parser_events::{Event, ScalarStyle};
use serde_json::{Value as Json, json};

const MAX_DEPTH: usize = 512;

struct Events<'input> {
    events: std::vec::IntoIter<Event<'input>>,
    anchors: BTreeMap<usize, Json>,
}

impl<'input> Events<'input> {
    fn next(&mut self) -> Result<Event<'input>, Box<dyn Error>> {
        loop {
            let event = self.events.next().ok_or("event stream ended early")?;
            if !matches!(event, Event::Nothing) {
                return Ok(event);
            }
        }
    }

    fn remember(&mut self, anchor: usize, node: &Json) {
        if anchor > 0 {
            self.anchors.insert(anchor, node.clone());
        }
    }

    /// Assemble one node of the typed tree from saphyr-parser events. Aliases are
    /// replaced by a copy of the anchored node; explicit tags are outside the
    /// controls' scope.
    fn node(&mut self, event: Event<'input>, depth: usize) -> Result<Json, Box<dyn Error>> {
        if depth > MAX_DEPTH {
            return Err("nesting deeper than the harness limit".into());
        }
        Ok(match event {
            Event::Scalar(text, style, anchor, tag) => {
                if tag.is_some() {
                    return Err("explicit tag outside the controls' scope".into());
                }
                let node = if style == ScalarStyle::Plain { plain(&text)? } else { json!(["str", text]) };
                self.remember(anchor, &node);
                node
            }
            Event::SequenceStart(anchor, tag) => {
                if tag.is_some() {
                    return Err("explicit tag outside the controls' scope".into());
                }
                let mut items = Vec::new();
                loop {
                    match self.next()? {
                        Event::SequenceEnd => break,
                        child => items.push(self.node(child, depth + 1)?),
                    }
                }
                let node = json!(["seq", items]);
                self.remember(anchor, &node);
                node
            }
            Event::MappingStart(anchor, tag) => {
                if tag.is_some() {
                    return Err("explicit tag outside the controls' scope".into());
                }
                let mut pairs = Vec::new();
                loop {
                    let key = match self.next()? {
                        Event::MappingEnd => break,
                        Event::Scalar(text, _, 0, None) => text.into_owned(),
                        _ => return Err("non-string mapping key".into()),
                    };
                    let event = self.next()?;
                    pairs.push(json!([key, self.node(event, depth + 1)?]));
                }
                let node = json!(["map", pairs]);
                self.remember(anchor, &node);
                node
            }
            Event::Alias(anchor) => self.anchors.get(&anchor).cloned().ok_or("unknown alias")?,
            _ => return Err("unexpected event".into()),
        })
    }
}

/// Parse YAML from local UTF-8 text with saphyr_parser::Parser::new_from_str (drained by
/// the src/events shim crate),
/// require exactly one document, and assemble its typed tree from the events.
pub fn parse(data: &[u8]) -> Result<Json, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let mut events = Events { events: parsarium_yaml_saphyr_parser_events::events(text)?.into_iter(), anchors: BTreeMap::new() };
    if !matches!(events.next()?, Event::StreamStart) || !matches!(events.next()?, Event::DocumentStart(_)) {
        return Err("expected a document".into());
    }
    let root = events.next()?;
    let tree = events.node(root, 0)?;
    if !matches!(events.next()?, Event::DocumentEnd) || !matches!(events.next()?, Event::StreamEnd) {
        return Err("expected exactly one document".into());
    }
    Ok(json!({"tree": tree}))
}

/// Harness-side typing of a plain scalar with the YAML 1.2 core-schema patterns
/// (null, bool, decimal/0o/0x int, finite float, otherwise str), as in the C and
/// C++ YAML harnesses. Quoted and block scalars are always str. The Parsarium
/// controls only use plain scalars that type the same under YAML 1.1 and 1.2.
fn plain(text: &str) -> Result<Json, Box<dyn Error>> {
    match text {
        "" | "~" | "null" | "Null" | "NULL" => return Ok(json!(["null"])),
        "true" | "True" | "TRUE" => return Ok(json!(["bool", true])),
        "false" | "False" | "FALSE" => return Ok(json!(["bool", false])),
        _ => {}
    }
    let digits = |s: &str, radix: u32| !s.is_empty() && s.chars().all(|c| c.is_digit(radix));
    let unsigned = text.strip_prefix(['-', '+']).unwrap_or(text);
    let int = if digits(unsigned, 10) {
        Some(text.parse::<i64>())
    } else if let Some(octal) = text.strip_prefix("0o").filter(|s| digits(s, 8)) {
        Some(i64::from_str_radix(octal, 8))
    } else if let Some(hex) = text.strip_prefix("0x").filter(|s| digits(s, 16)) {
        Some(i64::from_str_radix(hex, 16))
    } else {
        None
    };
    if let Some(int) = int {
        return Ok(json!(["int", int?.to_string()]));
    }
    if core_float(text) {
        let float: f64 = text.parse()?;
        if !float.is_finite() {
            return Err("non-finite float outside the typed tree".into());
        }
        return Ok(json!(["float", format!("{float}")]));
    }
    Ok(json!(["str", text]))
}

/// YAML 1.2 core schema float: [-+]?(\.[0-9]+|[0-9]+(\.[0-9]*)?)([eE][-+]?[0-9]+)?
fn core_float(text: &str) -> bool {
    let bytes = text.as_bytes();
    let mut i = 0;
    let mut mantissa = 0;
    if matches!(bytes.first(), Some(b'-' | b'+')) {
        i += 1;
    }
    while i < bytes.len() && bytes[i].is_ascii_digit() {
        i += 1;
        mantissa += 1;
    }
    if i < bytes.len() && bytes[i] == b'.' {
        i += 1;
        while i < bytes.len() && bytes[i].is_ascii_digit() {
            i += 1;
            mantissa += 1;
        }
    }
    if mantissa == 0 {
        return false;
    }
    if i < bytes.len() && matches!(bytes[i], b'e' | b'E') {
        i += 1;
        if i < bytes.len() && matches!(bytes[i], b'-' | b'+') {
            i += 1;
        }
        let start = i;
        while i < bytes.len() && bytes[i].is_ascii_digit() {
            i += 1;
        }
        if i == start {
            return false;
        }
    }
    i == bytes.len()
}
