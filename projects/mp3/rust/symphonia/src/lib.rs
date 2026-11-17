use std::error::Error;
use std::io::Cursor;

use symphonia::core::codecs::audio::AudioDecoderOptions;
use symphonia::core::formats::probe::Hint;
use symphonia::core::formats::{FormatOptions, TrackType};
use symphonia::core::io::MediaSourceStream;
use symphonia::core::meta::MetadataOptions;

/// Probe an untagged byte stream through the symphonia facade, then demux and decode every packet.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let source = MediaSourceStream::new(Box::new(Cursor::new(data.to_vec())), Default::default());
    let mut reader = symphonia::default::get_probe().probe(
        &Hint::new(), source, FormatOptions::default(), MetadataOptions::default())?;
    let format = reader.format_info().short_name;
    let track = reader.default_track(TrackType::Audio).ok_or("no audio track")?;
    let params = track.codec_params.as_ref().ok_or("no codec parameters")?.audio().ok_or("not audio")?.clone();
    let sample_rate = params.sample_rate.ok_or("no sample rate")?;
    let channels = params.channels.as_ref().ok_or("no channels")?.count();
    let mut decoder = symphonia::default::get_codecs()
        .make_audio_decoder(&params, &AudioDecoderOptions::default())?;
    let codec = decoder.codec_info().short_name;
    let (mut frames, mut frame_bytes, mut decoded_frames) = (0u64, 0u64, 0u64);
    while let Some(packet) = reader.next_packet()? {
        frames += 1;
        frame_bytes += packet.data.len() as u64;
        decoded_frames += decoder.decode(&packet)?.frames() as u64;
    }
    Ok(serde_json::json!({"format": format, "codec": codec, "sample_rate": sample_rate,
                          "channels": channels, "frames": frames, "frame_bytes": frame_bytes,
                          "decoded_frames": decoded_frames}))
}
