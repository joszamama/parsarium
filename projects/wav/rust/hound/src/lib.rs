use std::io::Cursor;

#[derive(Debug, PartialEq, Eq)]
pub struct Parsed {
    pub sample_rate: u32,
    pub channels: u16,
    pub samples: usize,
}

pub fn parse(data: &[u8]) -> Result<Parsed, Box<dyn std::error::Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input size outside harness limit".into());
    }
    let mut reader = hound::WavReader::new(Cursor::new(data))?;
    let spec = reader.spec();
    let mut samples = 0;
    for sample in reader.samples::<i16>() {
        let _ = sample?;
        samples += 1;
        if samples > (1 << 19) {
            return Err("sample count outside harness limit".into());
        }
    }
    Ok(Parsed { sample_rate: spec.sample_rate, channels: spec.channels, samples })
}
