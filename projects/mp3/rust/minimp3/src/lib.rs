use std::error::Error;
use std::io::Cursor;

use minimp3::{Decoder, Error as Mp3Error};
use sha2::{Digest, Sha256};

/// Decode every MPEG audio frame of an untagged MP3 byte stream through the minimp3 C decoder.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let mut decoder = Decoder::new(Cursor::new(data));
    let mut shapes = Vec::new();
    let mut bitrates = Vec::new();
    let (mut frames, mut samples_per_channel, mut pcm_samples) = (0u64, 0u64, 0u64);
    let mut pcm = Sha256::new();
    loop {
        let frame = match decoder.next_frame() {
            Ok(frame) => frame,
            Err(Mp3Error::Eof) => break,
            Err(error) => return Err(error.into()),
        };
        if frame.channels == 0 || frame.data.len() % frame.channels != 0 {
            return Err("decoded PCM is not a whole number of channel samples".into());
        }
        let shape = (frame.sample_rate, frame.channels, frame.layer);
        if !shapes.contains(&shape) {
            shapes.push(shape);
        }
        if !bitrates.contains(&frame.bitrate) {
            bitrates.push(frame.bitrate);
        }
        frames += 1;
        samples_per_channel += (frame.data.len() / frame.channels) as u64;
        pcm_samples += frame.data.len() as u64;
        for sample in &frame.data {
            pcm.update(sample.to_le_bytes());
        }
    }
    let &[(sample_rate, channels, layer)] = shapes.as_slice() else {
        return Err("no single sample rate, channel count and layer".into());
    };
    let bitrate_kbps = if let &[bitrate] = bitrates.as_slice() { Some(bitrate) } else { None };
    Ok(serde_json::json!({"sample_rate": sample_rate, "channels": channels, "layer": layer,
                          "bitrate_kbps": bitrate_kbps, "frames": frames,
                          "samples_per_channel": samples_per_channel, "pcm_samples": pcm_samples,
                          "pcm_sha256": format!("{:x}", pcm.finalize())}))
}
