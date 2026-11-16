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
        "async_zip" => {
            #[allow(deprecated)]
            pollster::block_on(async {
                let reader = upstream_async_zip::base::read::mem::ZipFileReader::new(bytes).await?;
                let entry = reader.file().entries().first().ok_or("no ZIP entry")?;
                let name = entry.filename().as_str()?.to_string();
                let size = entry.uncompressed_size();
                let mut content = String::new();
                futures_lite::io::AsyncReadExt::read_to_string(
                    &mut reader.reader_with_entry(0).await?, &mut content).await?;
                return Ok(output(&name, Some(&content), size));
                Ok::<(), Box<dyn Error>>(())
            })?;
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
    let outcome = parse_package("async_zip", &path);
    std::fs::remove_file(path)?;
    outcome
}
