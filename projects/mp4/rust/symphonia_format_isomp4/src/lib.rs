use std::error::Error;
use std::fs::File;
use std::path::Path;

fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let result = match package {
        "symphonia-format-isomp4" => {
            use symphonia::core::formats::{FormatOptions, FormatReader, TrackType};
            use symphonia::core::io::{MediaSourceStream, ReadBytes};
            let mut source = MediaSourceStream::new(Box::new(File::open(path)?), Default::default());
            source.read_quad_bytes()?;
            let mut movie = symphonia_format_isomp4::IsoMp4Reader::try_new(source, FormatOptions::default())?;
            let mut summary = serde_json::Map::new();
            let sample_rate = movie.default_track(TrackType::Audio).map(|track| {
                track.codec_params.as_ref().and_then(|params| params.audio()).and_then(|params| params.sample_rate)
            });
            if let Some(sample_rate) = sample_rate {
                if let Some(sample_rate) = sample_rate {
                    summary.insert("sample_rate".into(), sample_rate.into());
                }
                if let Some(packet) = movie.next_packet()? {
                    summary.insert("packet_bytes".into(), packet.data.len().into());
                }
            }
            serde_json::Value::Object(summary)
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
    let outcome = parse_package("symphonia-format-isomp4", &path);
    std::fs::remove_file(path)?;
    outcome
}
