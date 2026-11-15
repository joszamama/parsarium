# pure_wav — WAV / Rust

- **Pinned release:** `2.0.0`
- **License:** AGPL-3.0-or-later
- **Parsed scope:** WAV fmt/data chunks and declared sample count
- **Underlying family:** pure_wav parser
- **Local input API:** `Parser::default().read_instruction().process_data(&[u8])`
- **Documentation:** [API reference](<https://docs.rs/pure_wav/2.0.0/pure_wav/>)
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
