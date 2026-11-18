# waveadapter — WAV / Rust

- **Pinned release:** `0.3.1`
- **Upstream:** [source repository](<https://github.com/HEnquist/waveadapter>) · [crates.io](<https://crates.io/crates/waveadapter>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/rust/waveadapter/README.md)

```sh
python3 parsarium.py build wav rust waveadapter
python3 parsarium.py run wav rust waveadapter controls/wav/four-samples.wav
```
