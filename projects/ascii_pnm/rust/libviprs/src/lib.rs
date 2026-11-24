use serde_json::json;
use std::{
    env, fs,
    io::{BufReader, Cursor},
};

fn parse_package(package: &str, path: &std::path::Path) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    let args: Vec<String> = vec!["parser".into(), package.into(), path.to_string_lossy().into_owned()];
    if args.len() != 3 {
        return Err("usage: parsarium-rust-ascii-pnm PACKAGE CONTROL.pnm".into());
    }
    let bytes = fs::read(&args[2])?;
    let output = match args[1].as_str() {
        "libviprs" => {
            let img = libviprs::Raster::ppm_load(&bytes)?;
            // data() is the raster's native-endian buffer: one byte per sample
            // for maxval up to 255, two (Rgb16/Gray16) above. Report samples.
            let samples: Vec<u32> = match img.format().bytes_per_channel() {
                2 => img.data().chunks_exact(2)
                    .map(|b| u32::from(u16::from_ne_bytes([b[0], b[1]]))).collect(),
                4 => img.data().chunks_exact(4)
                    .map(|b| u32::from_ne_bytes([b[0], b[1], b[2], b[3]])).collect(),
                _ => img.data().iter().map(|&b| u32::from(b)).collect(),
            };
            json!({"width": img.width(), "height": img.height(), "rgb": samples})
        }
        other => return Err(format!("unknown package: {other}").into()),
    };
    Ok(output)
}

use std::sync::atomic::{AtomicU64, Ordering};
static NEXT_INPUT: AtomicU64 = AtomicU64::new(0);

pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let path = std::env::temp_dir().join(format!(
        "parsarium-rust-{}-{}.ppm",
        std::process::id(), NEXT_INPUT.fetch_add(1, Ordering::Relaxed)));
    std::fs::write(&path, data)?;
    let outcome = parse_package("libviprs", &path);
    std::fs::remove_file(path)?;
    outcome
}
