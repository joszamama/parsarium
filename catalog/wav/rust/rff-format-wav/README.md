# rff-format-wav — WAV / Rust

- **Pinned release:** `0.4.6`
- **License:** Apache-2.0
- **Parsed scope:** WAV track metadata and audio packet
- **Underlying family:** Remade FFmpeg WAV demuxer
- **Local input API:** `register(&mut FormatRegistry); open_demuxer("wav", File).read_header().read_packet()`
- **Documentation:** [API reference](<https://docs.rs/rff-format-wav/0.4.6/rff_format_wav/>)
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
