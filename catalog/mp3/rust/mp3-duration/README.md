# mp3-duration — MP3 / Rust

- **Pinned release:** `0.1.10`
- **Upstream:** [source repository](<https://github.com/agersant/mp3-duration>) · [crates.io](<https://crates.io/crates/mp3-duration>)
- **License:** MIT
- **Parsed scope:** MP3 frame-derived duration
- **Underlying family:** mp3-duration frame scanner
- **Local input API:** `from_path(path)`
- **Documentation:** [API reference](<https://docs.rs/mp3-duration/0.1.10/mp3_duration/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3/parsers.json) · [control verification](../../../../data/rust/mp3/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "duration_ms": 1152
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/rust/mp3_duration/README.md)

```sh
python3 parsarium.py build mp3 rust mp3_duration
python3 parsarium.py run mp3 rust mp3_duration controls/mp3/id3v2-tagged-tone.mp3
```
