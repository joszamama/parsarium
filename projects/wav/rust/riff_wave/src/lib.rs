use std::error::Error;
use std::fs::File;
use std::path::Path;

#[allow(deprecated)] // The pinned wav 1.0.1 reader is deprecated but remains a qualifying release.
fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let (sample_rate, channels, samples): (u32, u16, usize) = match package {
        "riff-wave" => {
            let mut reader = riff_wave::WaveReader::new(File::open(path)?)?;
            // WaveReader does not keep the data chunk length: it reads samples of
            // the header's bit depth until the input ends, so count those.
            let bits = reader.pcm_format.bits_per_sample;
            let mut count = 0usize;
            loop {
                let read = match bits {
                    8 => reader.read_sample_u8().map(|_| ()),
                    16 => reader.read_sample_i16().map(|_| ()),
                    24 => reader.read_sample_i24().map(|_| ()),
                    _ => reader.read_sample_i32().map(|_| ()),
                };
                match read {
                    Ok(()) => count += 1,
                    Err(error) if error.kind() == std::io::ErrorKind::UnexpectedEof => break,
                    Err(error) => return Err(error.into()),
                }
            }
            (reader.pcm_format.sample_rate, reader.pcm_format.num_channels, count)
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
    let outcome = parse_package("riff-wave", &path);
    std::fs::remove_file(path)?;
    outcome
}
