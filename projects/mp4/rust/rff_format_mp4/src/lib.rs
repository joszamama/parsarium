use std::error::Error;
use std::fs::File;
use std::path::Path;

fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let result = match package {
        "rff-format-mp4" => {
            let mut formats = rff_format::FormatRegistry::new();
            rff_format_mp4::register(&mut formats);
            let mut demuxer = formats.open_demuxer("mp4", Box::new(File::open(path)?))?;
            let streams = demuxer.read_header()?;
            serde_json::json!({"streams":streams.len()})
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
        "parsarium-rust-{}-{}.mp4",
        std::process::id(), NEXT_INPUT.fetch_add(1, Ordering::Relaxed)));
    std::fs::write(&path, data)?;
    let outcome = parse_package("rff-format-mp4", &path);
    std::fs::remove_file(path)?;
    outcome
}
