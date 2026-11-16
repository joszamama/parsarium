use std::error::Error;
use std::fs::File;
use std::path::Path;

fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let result = match package {
        "symphonia" => {
            use symphonia::core::formats::{FormatOptions, TrackType};
            use symphonia::core::formats::probe::Hint;
            use symphonia::core::io::MediaSourceStream;
            let source = MediaSourceStream::new(Box::new(File::open(path)?), Default::default());
            let mut hint = Hint::new();
            hint.with_extension("mp3");
            let mut reader = symphonia::default::get_probe().probe(&hint, source, FormatOptions::default(), Default::default())?;
            let track = reader.default_track(TrackType::Audio).ok_or("no audio track")?;
            let params = track.codec_params.as_ref().ok_or("no codec parameters")?.audio().ok_or("not audio")?;
            let sample_rate = params.sample_rate.ok_or("no sample rate")?;
            let channels = params.channels.as_ref().ok_or("no channels")?.count();
            let packet = reader.next_packet()?.ok_or("no audio packet")?;
            serde_json::json!({"sample_rate":sample_rate,"channels":channels,"packet_bytes":packet.data.len()})
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
    let outcome = parse_package("symphonia", &path);
    std::fs::remove_file(path)?;
    outcome
}
