use fltk::{image::PnmImage, prelude::ImageExt};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = std::env::args()
        .nth(1)
        .ok_or("usage: parsarium-rust-fltk-pnm CONTROL.pnm")?;
    let img = PnmImage::load(path)?;
    println!(
        "{}",
        serde_json::json!({"width": img.w(), "height": img.h(),
        "rgb": img.to_rgb_data()})
    );
    Ok(())
}
