# wav_io — WAV / Rust

- **Pinned release:** `0.1.17`
- **License:** MIT
- **Parsed scope:** PCM sample count and WAV metadata
- **Underlying family:** wav_io reader
- **Local input API:** `read_from_file(File)`
- **Documentation:** [API reference](<https://docs.rs/wav_io/0.1.17/wav_io/>)
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
