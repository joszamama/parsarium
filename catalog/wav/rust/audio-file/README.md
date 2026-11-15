# audio-file — WAV / Rust

- **Pinned release:** `0.5.1`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** Decoded PCM sample count and WAV metadata
- **Underlying family:** audio-file native WAV reader
- **Local input API:** `read::<f32>(path, ReadConfig::default())`
- **Documentation:** [API reference](<https://docs.rs/audio-file/0.5.1/audio_file/>)
- **Catalog evidence:** [parser record](../../../../data/rust/wav/parsers.json) · [control verification](../../../../data/rust/wav/verification.json) · [within-ecosystem ranking](../../../../data/rust/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "samples": 4
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
