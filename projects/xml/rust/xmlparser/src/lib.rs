use std::collections::{BTreeMap, BTreeSet};
use std::error::Error;
use xmlparser::{ElementEnd, Token, Tokenizer};

type Ns = BTreeMap<String, String>;

fn decode(raw: &str) -> Result<String, Box<dyn Error>> {
    let mut out = String::new();
    let mut rest = raw;
    while let Some(pos) = rest.find('&') {
        out.push_str(&rest[..pos]);
        let after = &rest[pos + 1..];
        let end = after.find(';').ok_or("unterminated XML reference")?;
        let name = &after[..end];
        match name {
            "amp" => out.push('&'),
            "lt" => out.push('<'),
            "gt" => out.push('>'),
            "quot" => out.push('"'),
            "apos" => out.push('\''),
            _ => {
                let number = if let Some(hex) = name.strip_prefix("#x") {
                    u32::from_str_radix(hex, 16)?
                } else if let Some(decimal) = name.strip_prefix('#') {
                    decimal.parse::<u32>()?
                } else {
                    return Err("external or undeclared entity outside harness scope".into());
                };
                out.push(char::from_u32(number).ok_or("invalid XML character reference")?);
            }
        }
        rest = &after[end + 1..];
    }
    out.push_str(rest);
    Ok(out)
}

fn expanded(ns: &Ns, prefix: &str, local: &str, attribute: bool) -> Result<String, Box<dyn Error>> {
    if prefix.is_empty() && attribute {
        return Ok(local.to_string());
    }
    let uri = ns.get(prefix).map(String::as_str).unwrap_or("");
    if !prefix.is_empty() && uri.is_empty() {
        return Err(format!("unbound XML prefix: {prefix}").into());
    }
    if uri.is_empty() {
        Ok(local.to_string())
    } else {
        Ok(format!("{{{uri}}}{local}"))
    }
}

/// Tokenize local UTF-8 XML with xmlparser. The adapter resolves namespaces,
/// XML references and element depth. serde_json encodes the summary only.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let input = std::str::from_utf8(data)?;
    let mut elements = Vec::new();
    let mut attributes = Vec::new();
    let mut namespaces = BTreeSet::new();
    let mut text_segments = Vec::new();
    let mut declarations = 0;
    let mut max_depth = 0;
    let mut stack: Vec<(String, Ns)> = Vec::new();
    let mut pending: Option<(String, String, Vec<(String, String, String)>)> = None;
    for token in Tokenizer::from(input) {
        match token? {
            Token::ElementStart { prefix, local, .. } => {
                if pending.is_some() {
                    return Err("unfinished XML start element".into());
                }
                pending = Some((prefix.as_str().into(), local.as_str().into(), Vec::new()));
            }
            Token::Attribute {
                prefix,
                local,
                value,
                ..
            } => {
                let item = pending.as_mut().ok_or("attribute outside start element")?;
                item.2.push((
                    prefix.as_str().into(),
                    local.as_str().into(),
                    value.as_str().into(),
                ));
            }
            Token::ElementEnd { end, .. } => match end {
                ElementEnd::Open | ElementEnd::Empty => {
                    let (prefix, local, attrs) =
                        pending.take().ok_or("missing XML start element")?;
                    let mut ns = stack
                        .last()
                        .map(|entry| entry.1.clone())
                        .unwrap_or_default();
                    ns.insert("xml".into(), "http://www.w3.org/XML/1998/namespace".into());
                    for (p, l, v) in &attrs {
                        if p == "xmlns" || (p.is_empty() && l == "xmlns") {
                            let key = if p == "xmlns" { l.as_str() } else { "" };
                            let uri = decode(v)?;
                            ns.insert(key.into(), uri.clone());
                            declarations += 1;
                            if !uri.is_empty() {
                                namespaces.insert(uri);
                            }
                        }
                    }
                    elements.push(expanded(&ns, &prefix, &local, false)?);
                    max_depth = max_depth.max(stack.len() + 1);
                    for (p, l, v) in attrs {
                        if p == "xmlns" || (p.is_empty() && l == "xmlns") {
                            continue;
                        }
                        attributes.push(format!(
                            "{}={}",
                            expanded(&ns, &p, &l, true)?,
                            decode(&v)?
                        ));
                    }
                    if matches!(end, ElementEnd::Open) {
                        stack.push((format!("{prefix}:{local}"), ns));
                    }
                }
                ElementEnd::Close(prefix, local) => {
                    let (name, _) = stack.pop().ok_or("extra XML close element")?;
                    if name != format!("{}:{}", prefix.as_str(), local.as_str()) {
                        return Err("mismatched XML close element".into());
                    }
                }
            },
            Token::Text { text } => {
                let decoded = decode(text.as_str())?;
                let trimmed = decoded.trim();
                if !trimmed.is_empty() {
                    text_segments.push(trimmed.to_string());
                }
            }
            Token::Cdata { text, .. } => {
                let trimmed = text.as_str().trim();
                if !trimmed.is_empty() {
                    text_segments.push(trimmed.to_string());
                }
            }
            _ => {}
        }
    }
    if pending.is_some() || !stack.is_empty() {
        return Err("incomplete XML tree".into());
    }
    let root = elements.first().ok_or("missing XML root")?.clone();
    Ok(serde_json::json!({"root": root, "elements": elements,
        "max_depth": max_depth, "namespace_declarations": declarations,
        "namespaces": namespaces, "attributes": attributes, "text": text_segments}))
}
