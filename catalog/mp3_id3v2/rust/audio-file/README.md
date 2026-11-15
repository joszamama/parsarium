# audio-file — MP3 with ID3v2 / Rust

- **Pinned release:** `0.5.1`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** Decoded MP3 audio samples
- **Underlying family:** audio-file via Symphonia
- **Local input API:** `read::<f32>(path, ReadConfig::default())`
- **Documentation:** [API reference](<https://docs.rs/audio-file/0.5.1/audio_file/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3_id3v2/parsers.json) · [control verification](../../../../data/rust/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "samples": 8000
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
