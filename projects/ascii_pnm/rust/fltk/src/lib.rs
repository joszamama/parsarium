use fltk::{image::PnmImage, prelude::ImageExt};
use serde_json::json;
use std::sync::atomic::{AtomicU64, Ordering};

static NEXT_INPUT: AtomicU64 = AtomicU64::new(0);

fn parse_path(path: &std::path::Path) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    let img = PnmImage::load(path)?;
    Ok(json!({"width": img.w(), "height": img.h(), "rgb": img.to_rgb_data()}))
}

/// The selected API only accepts a path, so each input is written to a private
/// temporary file and passed to `PnmImage::load` (FLTK `Fl_PNM_Image`).
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let path = std::env::temp_dir().join(format!(
        "parsarium-rust-fltk-{}-{}.ppm",
        std::process::id(), NEXT_INPUT.fetch_add(1, Ordering::Relaxed)));
    std::fs::write(&path, data)?;
    let outcome = parse_path(&path);
    std::fs::remove_file(path)?;
    outcome
}
