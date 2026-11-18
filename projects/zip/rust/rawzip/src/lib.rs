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
        "rawzip" => {
            let archive = rawzip::ZipArchive::from_slice(&bytes)?;
            let mut entries = archive.entries();
            // Read every entry in central-directory order; report the first one.
            let mut first: Option<(String, Vec<u8>, u64)> = None;
            while let Some(entry) = entries.next_entry()? {
                let normalized = entry.file_path().try_normalize()?;
                let name = normalized.as_ref().to_string();
                let size = entry.uncompressed_size_hint();
                let method = entry.compression_method();
                let local = archive.get_entry(entry.wayfinder())?;
                let mut content = Vec::new();
                // rawzip leaves decompression to the caller: inflate deflated
                // entries and pass stored entries through, as its docs show.
                if method == rawzip::CompressionMethod::STORE {
                    local.verifying_reader(local.data()).read_to_end(&mut content)?;
                } else if method == rawzip::CompressionMethod::DEFLATE {
                    let decoder = flate2::bufread::DeflateDecoder::new(local.data());
                    local.verifying_reader(decoder).read_to_end(&mut content)?;
                } else {
                    return Err(format!("unsupported ZIP compression method {method:?}").into());
                }
                if first.is_none() {
                    first = Some((name, content, size));
                }
            }
            let (name, content, size) = first.ok_or("no ZIP entry")?;
            let content = String::from_utf8(content).ok();
            return Ok(output(&name, content.as_deref(), size));
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
    let outcome = parse_package("rawzip", &path);
    std::fs::remove_file(path)?;
    outcome
}
