use serde_json::{Value, json};
use std::{env, fs, path::Path};

// The component parsers accept an SVG path-data value, rather than a document.
// This extraction is deliberately limited to the checked-in valid control.
fn path_data(text: &str) -> Result<&str, Box<dyn std::error::Error>> {
    let after = text.split_once("<path d=\"").ok_or("control has no path")?.1;
    Ok(after.split_once('"').ok_or("path attribute is not closed")?.0)
}

fn size_usvg(tree: &usvg::Tree) -> Value {
    json!({"width": tree.size().width(), "height": tree.size().height(),
           "nodes": tree.root().children().len()})
}

fn parse_package(package: &str, path: &std::path::Path) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    let args: Vec<String> = vec!["parser".into(), package.into(), path.to_string_lossy().into_owned()];
    if args.len() != 3 {
        return Err("usage: parsarium-rust-svg PACKAGE CONTROL.svg".into());
    }
    let package = args[1].as_str();
    let path = Path::new(&args[2]);
    let bytes = fs::read(path)?;
    let text = std::str::from_utf8(&bytes)?;
    let output = match package {
        "ps-usvg" => {
            let tree = ps_usvg::Tree::from_data(&bytes, &ps_usvg::Options::default())?;
            json!({"width": tree.size().width(), "height": tree.size().height(),
                   "nodes": tree.root().children().len()})
        }
        _ => return Err(format!("unknown package: {package}").into()),
    };
    Ok(output)
}

use std::sync::atomic::{AtomicU64, Ordering};
static NEXT_INPUT: AtomicU64 = AtomicU64::new(0);

pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let path = std::env::temp_dir().join(format!(
        "parsarium-rust-{}-{}.svg",
        std::process::id(), NEXT_INPUT.fetch_add(1, Ordering::Relaxed)));
    std::fs::write(&path, data)?;
    let outcome = parse_package("ps-usvg", &path);
    std::fs::remove_file(path)?;
    outcome
}
