#[derive(Debug, PartialEq, Eq)]
pub struct Parsed {
    pub width: u32,
    pub height: u32,
    pub rgb: Vec<u8>,
}

pub fn parse(data: &[u8]) -> Result<Parsed, Box<dyn std::error::Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input size outside harness limit".into());
    }
    let image = image::load_from_memory_with_format(data, image::ImageFormat::Pnm)?;
    let width = image.width();
    let height = image.height();
    if width == 0 || height == 0 || width > 4096 || height > 4096 {
        return Err("dimensions outside harness limit".into());
    }
    let pixels = image.to_rgb8();
    let rgb = pixels.as_raw().iter().take(6).copied().collect();
    Ok(Parsed { width, height, rgb })
}
