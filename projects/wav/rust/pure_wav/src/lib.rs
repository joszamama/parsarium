use std::error::Error;
use std::fs::File;
use std::path::Path;

#[allow(deprecated)] // The pinned wav 1.0.1 reader is deprecated but remains a qualifying release.
fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let (sample_rate, channels, samples): (u32, u16, usize) = match package {
        "pure_wav" => {
            let data = std::fs::read(path)?;
            let mut parser = pure_wav::Parser::default();
            loop {
                let step = parser.read_instruction();
                let start = step.position as usize;
                let end = start + step.len as usize;
                match parser.process_data(&data[start..end]).map_err(|e| format!("{e:?}"))? {
                    pure_wav::ProcessDataOutput::Done(meta) => {
                        let channels = meta.fmt.n_channels.get();
                        let samples = meta.data_len as usize / (meta.fmt.w_bits_per_sample.get() as usize / 8);
                        break (meta.fmt.n_samples_per_sec.get(), channels, samples);
                    }
                    pure_wav::ProcessDataOutput::InProgress(next) => parser = next,
                }
            }
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
    let outcome = parse_package("pure_wav", &path);
    std::fs::remove_file(path)?;
    outcome
}
