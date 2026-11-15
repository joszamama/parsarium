# audio-file — MP4 / Rust

- **Pinned release:** `0.5.1`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** MP4 AAC decoded audio
- **Underlying family:** Symphonia ISO-MP4 wrapper
- **Local input API:** `read::<f32>(path, ReadConfig::default())`
- **Documentation:** [API reference](<https://docs.rs/audio-file/0.5.1/audio_file/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "samples": 9216
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
