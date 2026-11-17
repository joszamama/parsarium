use std::error::Error;
use std::mem::MaybeUninit;

use serde_json::{Value as Json, json};
use unsafe_libyaml::{
    YAML_MAPPING_NODE, YAML_PLAIN_SCALAR_STYLE, YAML_SCALAR_NODE, YAML_SEQUENCE_NODE, yaml_document_delete,
    yaml_document_get_node, yaml_document_get_root_node, yaml_document_t, yaml_node_t, yaml_parser_delete,
    yaml_parser_initialize, yaml_parser_load, yaml_parser_set_input_string, yaml_parser_t,
};

const MAX_DEPTH: usize = 512;

unsafe fn scalar_text<'a>(node: *const yaml_node_t) -> Result<&'a str, Box<dyn Error>> {
    let scalar = unsafe { (*node).data.scalar };
    let bytes = unsafe { std::slice::from_raw_parts(scalar.value, scalar.length as usize) };
    Ok(std::str::from_utf8(bytes)?)
}

/// Walk libyaml's composed node graph (yaml_parser_load) into the typed tree.
/// The loader already points aliases at the anchored node; the default tags it
/// assigns are not used, and plain scalars are typed by the harness.
unsafe fn walk(document: *mut yaml_document_t, node: *mut yaml_node_t, depth: usize) -> Result<Json, Box<dyn Error>> {
    if node.is_null() {
        return Err("missing node".into());
    }
    if depth > MAX_DEPTH {
        return Err("nesting deeper than the harness limit".into());
    }
    unsafe {
        Ok(match (*node).type_ {
            YAML_SCALAR_NODE => {
                let text = scalar_text(node)?;
                if (*node).data.scalar.style == YAML_PLAIN_SCALAR_STYLE { plain(text)? } else { json!(["str", text]) }
            }
            YAML_SEQUENCE_NODE => {
                let items = (*node).data.sequence.items;
                let mut nodes = Vec::new();
                let mut item = items.start;
                while item < items.top {
                    nodes.push(walk(document, yaml_document_get_node(document, *item), depth + 1)?);
                    item = item.add(1);
                }
                json!(["seq", nodes])
            }
            YAML_MAPPING_NODE => {
                let pairs_stack = (*node).data.mapping.pairs;
                let mut pairs = Vec::new();
                let mut pair = pairs_stack.start;
                while pair < pairs_stack.top {
                    let key = yaml_document_get_node(document, (*pair).key);
                    if key.is_null() || (*key).type_ != YAML_SCALAR_NODE {
                        return Err("non-string mapping key".into());
                    }
                    let value = walk(document, yaml_document_get_node(document, (*pair).value), depth + 1)?;
                    pairs.push(json!([scalar_text(key)?, value]));
                    pair = pair.add(1);
                }
                json!(["map", pairs])
            }
            _ => return Err("empty node".into()),
        })
    }
}

/// Parse YAML from local UTF-8 bytes with unsafe-libyaml's documented loader API
/// (yaml_parser_initialize, yaml_parser_set_input_string, yaml_parser_load),
/// require exactly one document, and report its typed tree.
pub fn parse(data: &[u8]) -> Result<Json, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    std::str::from_utf8(data)?;
    unsafe {
        let mut parser = MaybeUninit::<yaml_parser_t>::uninit();
        if yaml_parser_initialize(parser.as_mut_ptr()).fail {
            return Err("parser initialization failed".into());
        }
        let parser = parser.as_mut_ptr();
        yaml_parser_set_input_string(parser, data.as_ptr(), data.len() as _);
        let mut document = MaybeUninit::<yaml_document_t>::uninit();
        if yaml_parser_load(parser, document.as_mut_ptr()).fail {
            yaml_parser_delete(parser);
            return Err("libyaml could not load the document".into());
        }
        let document = document.as_mut_ptr();
        let root = yaml_document_get_root_node(document);
        let tree = if root.is_null() { Err("empty stream".into()) } else { walk(document, root, 0) };
        yaml_document_delete(document);
        let tree = match tree {
            Ok(tree) => tree,
            Err(error) => {
                yaml_parser_delete(parser);
                return Err(error);
            }
        };
        let mut next = MaybeUninit::<yaml_document_t>::uninit();
        let loaded = !yaml_parser_load(parser, next.as_mut_ptr()).fail;
        let single = loaded && yaml_document_get_root_node(next.as_mut_ptr()).is_null();
        if loaded {
            yaml_document_delete(next.as_mut_ptr());
        }
        yaml_parser_delete(parser);
        if !single {
            return Err("expected exactly one document".into());
        }
        Ok(json!({"tree": tree}))
    }
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
