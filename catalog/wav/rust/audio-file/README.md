# audio-file — WAV / Rust

- **Pinned release:** `0.5.1`
- **Upstream:** [source repository](<https://github.com/neodsp/audio-file>) · [crates.io](<https://crates.io/crates/audio-file>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/rust/audio_file/README.md)

```sh
python3 parsarium.py build wav rust audio_file
python3 parsarium.py run wav rust audio_file controls/wav/four-samples.wav
```
