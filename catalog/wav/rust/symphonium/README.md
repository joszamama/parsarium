# symphonium — WAV / Rust

- **Pinned release:** `0.13.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** WAV track metadata and declared frames
- **Underlying family:** Symphonia WAV demuxer
- **Local input API:** `probe_from_file(path, None).format_reader()`
- **Documentation:** [API reference](<https://docs.rs/symphonium/0.13.0/symphonium/>)
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

[Docker harness and verification receipt](../../../../projects/wav/rust/symphonium/README.md)

```sh
python3 parsarium.py build wav rust symphonium
python3 parsarium.py run wav rust symphonium controls/wav/four-samples.wav
```
