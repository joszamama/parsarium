# wave_stream — WAV / Rust

- **Pinned release:** `0.6.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** WAV metadata and first decoded sample
- **Underlying family:** wave_stream reader
- **Local input API:** `read_wav_from_file_path(path).get_random_access_f32_reader().read_sample(0)`
- **Documentation:** [API reference](<https://docs.rs/wave_stream/0.6.0/wave_stream/>)
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
