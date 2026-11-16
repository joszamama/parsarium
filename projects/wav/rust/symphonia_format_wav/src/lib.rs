use std::error::Error;
use std::fs::File;
use std::path::Path;

#[allow(deprecated)] // The pinned wav 1.0.1 reader is deprecated but remains a qualifying release.
fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let (sample_rate, channels, samples): (u32, u16, usize) = match package {
        "symphonia-format-wav" => {
            use symphonia_core_05::formats::FormatReader;
            use symphonia_core_05::io::MediaSourceStream;
            let source = MediaSourceStream::new(Box::new(File::open(path)?), Default::default());
            #[allow(deprecated)]
            let mut reader = symphonia_format_wav::WavReader::try_new(source, &Default::default())?;
            let track = reader.tracks().first().ok_or("no audio track")?;
            let params = &track.codec_params;
            let sample_rate = params.sample_rate.ok_or("no sample rate")?;
            let channels = params.channels.ok_or("no channels")?.count() as u16;
            let frames = params.n_frames.ok_or("no frame count")?;
            assert!(reader.next_packet().is_ok());
            (sample_rate, channels, frames as usize * channels as usize)
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
    let outcome = parse_package("symphonia-format-wav", &path);
    std::fs::remove_file(path)?;
    outcome
}
