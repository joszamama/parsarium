use std::error::Error;
use std::fs::File;
use std::path::Path;

fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let result = match package {
        "oxideav-mp4" => {
            use oxideav_core::{ReadSeek, RuntimeContext};
            let mut context = RuntimeContext::new();
            oxideav_mp4::register(&mut context);
            let input: Box<dyn ReadSeek> = Box::new(File::open(path)?);
            let demuxer = context.containers.open_demuxer("mp4", input, &context.codecs)?;
            serde_json::json!({"streams":demuxer.streams().len()})
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
    let outcome = parse_package("oxideav-mp4", &path);
    std::fs::remove_file(path)?;
    outcome
}
