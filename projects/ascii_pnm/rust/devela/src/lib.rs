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
        "devela" => {
            let len = devela::Pnm::decoded_len_u8(&bytes).map_err(|e| format!("{e:?}"))?;
            let mut pixels = vec![0; len];
            let (size, channels) =
                devela::Pnm::decode_u8(&bytes, &mut pixels).map_err(|e| format!("{e:?}"))?;
            json!({"size": format!("{size:?}"), "channels": channels, "pixels": pixels})
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
    let outcome = parse_package("devela", &path);
    std::fs::remove_file(path)?;
    outcome
}
