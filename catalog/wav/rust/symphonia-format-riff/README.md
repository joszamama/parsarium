# symphonia-format-riff — WAV / Rust

- **Pinned release:** `0.6.1`
- **License:** MPL-2.0
- **Parsed scope:** WAV track metadata and audio packet
- **Underlying family:** Symphonia WAV demuxer
- **Local input API:** `WavReader::try_new(MediaSourceStream, FormatOptions).next_packet()`
- **Documentation:** [API reference](<https://docs.rs/symphonia-format-riff/0.6.1/symphonia_format_riff/>)
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
