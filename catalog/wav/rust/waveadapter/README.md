# waveadapter — WAV / Rust

- **Pinned release:** `0.3.1`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** WAV metadata and declared frame length
- **Underlying family:** waveadapter reader
- **Local input API:** `WavReader::new(File).sample_rate().frames()`
- **Documentation:** [API reference](<https://docs.rs/waveadapter/0.3.1/waveadapter/>)
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
