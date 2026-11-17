use std::error::Error;

use rusty_mp3::{Error as Mp3Error, Mp3Decoder};
use sha2::{Digest, Sha256};

/// Push an untagged MP3 byte stream into the streaming decoder and drain every decoded frame.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let mut decoder = Mp3Decoder::new();
    decoder.push(data);
    decoder.flush();
    let mut shapes = Vec::new();
    let (mut frames, mut samples_per_channel, mut pcm_samples) = (0u64, 0u64, 0u64);
    let mut pcm = Sha256::new();
    loop {
        let frame = match decoder.next_frame() {
            Ok(frame) => frame,
            Err(Mp3Error::Eof) => break,
            Err(error) => return Err(error.into()),
        };
        let channels = usize::from(frame.channels);
        if channels == 0 || frame.samples.len() % channels != 0 {
            return Err("decoded PCM is not a whole number of channel samples".into());
        }
        let shape = (frame.sample_rate, frame.channels);
        if !shapes.contains(&shape) {
            shapes.push(shape);
        }
        frames += 1;
        samples_per_channel += (frame.samples.len() / channels) as u64;
        pcm_samples += frame.samples.len() as u64;
        for sample in &frame.samples {
            pcm.update(sample.to_le_bytes());
        }
    }
    let &[(sample_rate, channels)] = shapes.as_slice() else {
        return Err("no single sample rate and channel count".into());
    };
    Ok(serde_json::json!({"sample_rate": sample_rate, "channels": channels, "frames": frames,
                          "samples_per_channel": samples_per_channel, "pcm_samples": pcm_samples,
                          "pcm_f32_sha256": format!("{:x}", pcm.finalize())}))
}
