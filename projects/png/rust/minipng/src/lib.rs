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
        "minipng" => {
            let header = minipng::decode_png_header(&bytes)?;
            let mut buffer = vec![0; header.required_bytes_rgba8bpc()];
            let mut image = minipng::decode_png(&bytes, &mut buffer)?;
            image.convert_to_rgba8bpc()?;
            return Ok(serde_json::from_str(&format!("{{\"width\":{},\"height\":{},\"red_0_0\":{}}}", image.width(), image.height(), image.pixels()[0]))?);
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
    let outcome = parse_package("minipng", &path);
    std::fs::remove_file(path)?;
    outcome
}
