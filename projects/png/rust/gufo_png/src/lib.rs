use std::error::Error;
use std::fs;
use std::io::{BufReader, Cursor};

fn parse_package(package: &str, path: &std::path::Path) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    let args: Vec<String> = std::vec!["parser".into(), package.into(), path.to_string_lossy().into_owned()];
    if args.len() != 3 {
        return Err("usage: cargo run -- PACKAGE CONTROL".into());
    }
    let name = &args[1];
    let bytes = fs::read(&args[2])?;
    match name.as_str() {
        "gufo-png" => {
            let image = gufo_png::Png::new(bytes).map_err(|error| format!("{error:?}"))?;
            // The first tEXt chunk, when the file has one; an empty object otherwise.
            let Some(title) = image.chunks().into_iter()
                .find(|chunk| chunk.chunk_type() == gufo_png::ChunkType::tEXt) else {
                return Ok(serde_json::json!({}));
            };
            let (key, value) = title.text()?;
            // tEXt keywords and text are ISO 8859-1.
            let latin1 = |bytes: &[u8]| bytes.iter().map(|&byte| byte as char).collect::<String>();
            return Ok(serde_json::json!({"key": latin1(key), "value": latin1(value)}));
        }
        _ => return Err(format!("unknown PNG package: {name}").into()),
    }
    Err("parser produced no result".into())
}

use std::sync::atomic::{AtomicU64, Ordering};
static NEXT_INPUT: AtomicU64 = AtomicU64::new(0);

pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let path = std::env::temp_dir().join(format!(
        "parsarium-rust-{}-{}.png",
        std::process::id(), NEXT_INPUT.fetch_add(1, Ordering::Relaxed)));
    std::fs::write(&path, data)?;
    let outcome = parse_package("gufo-png", &path);
    std::fs::remove_file(path)?;
    outcome
}
