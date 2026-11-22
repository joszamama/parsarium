use std::error::Error;
use std::fs::File;
use std::path::Path;

#[allow(deprecated)] // The pinned wav 1.0.1 reader is deprecated but remains a qualifying release.
fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let (sample_rate, channels, samples): (u32, u16, usize) = match package {
        "wavers" => {
            let (values, sample_rate) = wavers::read::<i16, _>(path)?;
            let reader = wavers::Wav::<i16>::from_path(path)?;
            (sample_rate as u32, reader.n_channels(), values.len())
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
    let outcome = parse_package("wavers", &path);
    std::fs::remove_file(path)?;
    outcome
}
