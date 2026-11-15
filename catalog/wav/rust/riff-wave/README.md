# riff-wave — WAV / Rust

- **Pinned release:** `0.1.3`
- **License:** Apache-2.0
- **Parsed scope:** Decoded PCM sample values and WAV metadata
- **Underlying family:** riff-wave reader
- **Local input API:** `WaveReader::new(File).read_sample_i16()`
- **Documentation:** [API reference](<https://docs.rs/riff-wave/0.1.3/riff_wave/>)
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
