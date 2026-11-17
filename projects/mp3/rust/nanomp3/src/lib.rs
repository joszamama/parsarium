use std::error::Error;

use nanomp3::{Channels, Decoded, Options};
use sha2::{Digest, Sha256};

fn pcm_sha256(samples: &[i16]) -> String {
    let mut pcm = Sha256::new();
    for sample in samples {
        pcm.update(sample.to_le_bytes());
    }
    format!("{:x}", pcm.finalize())
}

/// Walk every MPEG audio frame of an untagged MP3 byte slice, then decode the whole slice to i16 PCM,
/// once with nanomp3's defaults and once with its documented minimp3-compatible i16 rounding.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let mut shapes = Vec::new();
    let mut bitrates = Vec::new();
    let (mut frames, mut frame_bytes, mut frame_samples) = (0u64, 0u64, 0u64);
    for frame in nanomp3::frames(data) {
        let channels = match frame.channels {
            Channels::Mono => 1u8,
            Channels::Stereo => 2u8,
        };
        let shape = (frame.sample_rate, channels, frame.layer);
        if !shapes.contains(&shape) {
            shapes.push(shape);
        }
        if !bitrates.contains(&frame.bitrate_kbps) {
            bitrates.push(frame.bitrate_kbps);
        }
        frames += 1;
        frame_bytes += frame.data.len() as u64;
        frame_samples += frame.samples as u64;
    }
    let &[(sample_rate, channels, layer)] = shapes.as_slice() else {
        return Err("no single sample rate, channel count and layer".into());
    };
    let decoded: Decoded<i16> = nanomp3::decode_all(data);
    let compat: Decoded<i16> = nanomp3::decode_all_with(data, Options::default().minimp3_compat(true));
    for result in [&decoded, &compat] {
        let decoded_channels = match result.channels {
            Some(Channels::Mono) => 1u8,
            Some(Channels::Stereo) => 2u8,
            None => return Err("no decoded audio".into()),
        };
        if result.format_changed || (result.sample_rate, decoded_channels, result.layer) != (sample_rate, channels, layer)
            || result.samples.len() % usize::from(channels) != 0 {
            return Err("decoded stream disagrees with its frames".into());
        }
    }
    let bitrate_kbps = if let &[bitrate] = bitrates.as_slice() { Some(bitrate) } else { None };
    Ok(serde_json::json!({"sample_rate": sample_rate, "channels": channels, "layer": layer,
                          "bitrate_kbps": bitrate_kbps, "frames": frames, "frame_bytes": frame_bytes,
                          "frame_samples_per_channel": frame_samples,
                          "samples_per_channel": decoded.samples.len() / usize::from(channels),
                          "pcm_samples": decoded.samples.len(),
                          "pcm_sha256": pcm_sha256(&decoded.samples),
                          "minimp3_compat_pcm_sha256": pcm_sha256(&compat.samples)}))
}
