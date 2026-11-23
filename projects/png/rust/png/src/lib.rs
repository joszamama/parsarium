use std::io::{BufReader, Cursor};

#[derive(Debug, PartialEq, Eq)]
pub struct Parsed {
    pub width: u32,
    pub height: u32,
    pub red_0_0: u8,
}

pub fn parse(data: &[u8]) -> Result<Parsed, Box<dyn std::error::Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input size outside harness limit".into());
    }
    let mut decoder = png::Decoder::new(BufReader::new(Cursor::new(data)));
    // Without EXPAND the output buffer holds palette indices and packed 1-4 bit
    // samples, so its first byte is not a red sample. EXPAND is the crate's own
    // palette, tRNS and low-bit-depth expansion; 16-bit samples stay 16-bit and
    // the first byte is the high byte of red (or grey).
    decoder.set_transformations(png::Transformations::EXPAND);
    let mut reader = decoder.read_info()?;
    let size = reader.output_buffer_size().ok_or("no output buffer size")?;
    if size == 0 || size > (1 << 22) {
        return Err("decoded output outside harness limit".into());
    }
    let mut buffer = vec![0; size];
    let frame = reader.next_frame(&mut buffer)?;
    Ok(Parsed {
        width: frame.width,
        height: frame.height,
        red_0_0: buffer[0],
    })
}
