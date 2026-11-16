use std::error::Error;
use std::fs::File;
use std::path::Path;

fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let result = match package {
        "rmp3" => {
            let bytes = std::fs::read(path)?;
            let mut reader = rmp3::Decoder::new(&bytes);
            let audio = loop {
                match reader.next() {
                    Some(rmp3::Frame::Audio(audio)) => break (audio.sample_rate(),audio.channels(),audio.sample_count()),
                    Some(rmp3::Frame::Other(_)) => continue,
                    None => return Err("no audio frame".into()),
                }
            };
            serde_json::json!({"sample_rate":audio.0,"channels":audio.1,"samples_per_channel":audio.2})
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
    let outcome = parse_package("rmp3", &path);
    std::fs::remove_file(path)?;
    outcome
}
