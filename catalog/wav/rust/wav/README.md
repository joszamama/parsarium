# wav — WAV / Rust

- **Pinned release:** `1.0.1`
- **License:** LGPL-3.0
- **Parsed scope:** Decoded PCM sample values and WAV metadata
- **Underlying family:** wav legacy reader
- **Local input API:** `read(&mut File)`
- **Documentation:** [API reference](<https://docs.rs/wav/1.0.1/wav/>)
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
