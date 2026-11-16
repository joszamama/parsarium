use std::error::Error;
use std::fs::File;
use std::path::Path;

fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let result = match package {
        "id3-core" => {
            let bytes = std::fs::read(path)?;
            let tag = id3_core::Tag::parse(&bytes)?;
            serde_json::json!({"version":tag.major_version,"title":tag.text_field(id3_core::TextField::Title),"artist":tag.text_field(id3_core::TextField::Artist)})
        }
        _ => return Err(format!("unknown package: {package}").into()),
    };
    Ok(result)
}


use std::sync::atomic::{AtomicU64, Ordering};
static NEXT_INPUT: AtomicU64 = AtomicU64::new(0);

pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let path = std::env::temp_dir().join(format!(
        "parsarium-rust-{}-{}.mp3",
        std::process::id(), NEXT_INPUT.fetch_add(1, Ordering::Relaxed)));
    std::fs::write(&path, data)?;
    let outcome = parse_package("id3-core", &path);
    std::fs::remove_file(path)?;
    outcome
}
