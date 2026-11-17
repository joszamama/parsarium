use std::error::Error;
use std::io::Cursor;

use symphonia_bundle_mp3::{MpaDecoder, MpaReader};
use symphonia_core::codecs::audio::{AudioDecoder, AudioDecoderOptions};
use symphonia_core::formats::{FormatOptions, FormatReader, TrackType};
use symphonia_core::io::MediaSourceStream;

/// Demux every MPEG audio frame of an untagged MP3 byte stream and decode it.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let source = MediaSourceStream::new(Box::new(Cursor::new(data.to_vec())), Default::default());
    let mut reader = MpaReader::try_new(source, FormatOptions::default())?;
    let track = reader.default_track(TrackType::Audio).ok_or("no audio track")?;
    let params = track.codec_params.as_ref().ok_or("no codec parameters")?.audio().ok_or("not audio")?.clone();
    let sample_rate = params.sample_rate.ok_or("no sample rate")?;
    let channels = params.channels.as_ref().ok_or("no channels")?.count();
    let mut decoder = MpaDecoder::try_new(&params, &AudioDecoderOptions::default())?;
    let (mut frames, mut frame_bytes, mut decoded_frames) = (0u64, 0u64, 0u64);
    while let Some(packet) = reader.next_packet()? {
        frames += 1;
        frame_bytes += packet.data.len() as u64;
        decoded_frames += decoder.decode(&packet)?.frames() as u64;
    }
    Ok(serde_json::json!({"sample_rate": sample_rate, "channels": channels, "frames": frames,
                          "frame_bytes": frame_bytes, "decoded_frames": decoded_frames}))
}
