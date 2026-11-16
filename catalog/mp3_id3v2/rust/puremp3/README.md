# puremp3 — MP3 with ID3v2 / Rust

- **Pinned release:** `0.1.0`
- **License:** MIT OR CC0-1.0
- **Parsed scope:** Decoded MP3 sample and frame header
- **Underlying family:** puremp3 decoder
- **Local input API:** `read_mp3(File).next()`
- **Documentation:** [API reference](<https://docs.rs/puremp3/0.1.0/puremp3/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3_id3v2/parsers.json) · [control verification](../../../../data/rust/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/rust/puremp3/README.md)

```sh
python3 parsarium.py build mp3_id3v2 rust puremp3
python3 parsarium.py run mp3_id3v2 rust puremp3 controls/mp3_id3v2/tone-tags.mp3
```
