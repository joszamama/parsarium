use std::error::Error;
use std::fs::File;
use std::path::Path;

fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let result = match package {
        "nanomp3" => {
            let bytes = std::fs::read(path)?;
            let audio = nanomp3::decode_all::<i16>(&bytes);
            if audio.samples.is_empty() { return Err("no decoded samples".into()); }
            serde_json::json!({"sample_rate":audio.sample_rate,"layer":audio.layer,"samples":audio.samples.len()})
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
    let outcome = parse_package("nanomp3", &path);
    std::fs::remove_file(path)?;
    outcome
}
