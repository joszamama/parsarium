use std::error::Error;
use std::fs::File;
use std::path::Path;

#[allow(deprecated)] // The pinned wav 1.0.1 reader is deprecated but remains a qualifying release.
fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let (sample_rate, channels, samples): (u32, u16, usize) = match package {
        "symphonium" => {
            let source = symphonium::probe_from_file(path, None)?;
            let sample_rate = source.sample_rate().ok_or("no sample rate")?.get();
            let track = source.format_reader().default_track(symphonia::core::formats::TrackType::Audio).ok_or("no audio track")?;
            let frames = track.num_frames.ok_or("no frame count")?;
            (sample_rate, source.num_channels().get() as u16, frames as usize * source.num_channels().get())
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
    let outcome = parse_package("symphonium", &path);
    std::fs::remove_file(path)?;
    outcome
}
