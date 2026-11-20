use std::error::Error;
use std::fs::File;
use std::path::Path;

fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let result = match package {
        "lofty" => {
            use lofty::file::TaggedFileExt;
            use lofty::tag::Accessor;
            let file = lofty::read_from_path(path)?;
            // A file without a tag of the primary type (ID3v2 for MPEG) has no tag fields.
            match file.primary_tag() {
                Some(tag) => serde_json::json!({"title":tag.title(), "artist":tag.artist(), "album":tag.album()}),
                None => serde_json::json!({}),
            }
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
    let outcome = parse_package("lofty", &path);
    std::fs::remove_file(path)?;
    outcome
}
