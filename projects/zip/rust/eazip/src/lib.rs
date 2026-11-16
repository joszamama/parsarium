use std::error::Error;
use std::fs;
use std::io::{Cursor, Read};

fn output(name: &str, content: Option<&str>, size: u64) -> serde_json::Value {
    serde_json::json!({"name": name, "content": content, "size": size})
}

fn output_entry(name: &str, count: usize) -> serde_json::Value {
    serde_json::json!({"name": name, "entry_count": count})
}

fn parse_package(package: &str, path: &std::path::Path) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    let args: Vec<String> = std::vec!["parser".into(), package.into(), path.to_string_lossy().into_owned()];
    if args.len() != 3 {
        return Err("usage: parsarium-rust-zip PACKAGE CONTROL".into());
    }
    let bytes = fs::read(&args[2])?;
    match args[1].as_str() {
        "eazip" => {
            let mut archive = eazip::ArchiveReader::open(&args[2])?;
            let mut entry = archive.get_by_index(0).ok_or("no ZIP entry")?;
            let name = entry.metadata().name().to_string();
            let size = entry.metadata().uncompressed_size;
            let mut content = String::new();
            entry.read()?.read_to_string(&mut content)?;
            return Ok(output(&name, Some(&content), size));
        }
        other => return Err(format!("unknown ZIP package: {other}").into()),
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
        "parsarium-rust-{}-{}.zip",
        std::process::id(), NEXT_INPUT.fetch_add(1, Ordering::Relaxed)));
    std::fs::write(&path, data)?;
    let outcome = parse_package("eazip", &path);
    std::fs::remove_file(path)?;
    outcome
}
