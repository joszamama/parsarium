use std::error::Error;
use std::fs::File;
use std::path::Path;

#[allow(deprecated)] // The pinned wav 1.0.1 reader is deprecated but remains a qualifying release.
fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let (sample_rate, channels, samples): (u32, u16, usize) = match package {
        "rff-format-wav" => {
            let mut registry = rff_format::FormatRegistry::new();
            rff_format_wav::register(&mut registry);
            let mut reader = registry.open_demuxer("wav", Box::new(File::open(path)?))?;
            let tracks = reader.read_header()?;
            let track = tracks.first().ok_or("no audio track")?;
            let sample_rate = track.sample_rate;
            let channels = track.channels;
            let packet = reader.read_packet()?;
            (sample_rate, channels, packet.duration as usize * channels as usize)
        }
        _ => return Err(format!("unknown package: {package}").into()),
    };
    Ok(serde_json::json!({"sample_rate": sample_rate, "channels": channels, "samples": samples}))
}


use std::sync::atomic::{AtomicU64, Ordering};
static NEXT_INPUT: AtomicU64 = AtomicU64::new(0);

pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let path = std::env::temp_dir().join(format!(
        "parsarium-rust-{}-{}.wav",
        std::process::id(), NEXT_INPUT.fetch_add(1, Ordering::Relaxed)));
    std::fs::write(&path, data)?;
    let outcome = parse_package("rff-format-wav", &path);
    std::fs::remove_file(path)?;
    outcome
}
