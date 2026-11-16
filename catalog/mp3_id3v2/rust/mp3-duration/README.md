# mp3-duration — MP3 with ID3v2 / Rust

- **Pinned release:** `0.1.10`
- **License:** MIT
- **Parsed scope:** MP3 frame-derived duration
- **Underlying family:** mp3-duration frame scanner
- **Local input API:** `from_path(path)`
- **Documentation:** [API reference](<https://docs.rs/mp3-duration/0.1.10/mp3_duration/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3_id3v2/parsers.json) · [control verification](../../../../data/rust/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "duration_ms": 1152
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/rust/mp3_duration/README.md)

```sh
python3 parsarium.py build mp3_id3v2 rust mp3_duration
python3 parsarium.py run mp3_id3v2 rust mp3_duration controls/mp3_id3v2/tone-tags.mp3
```
