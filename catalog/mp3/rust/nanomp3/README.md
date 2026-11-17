# nanomp3 — MP3 / Rust

- **Pinned release:** `0.2.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** Decoded MP3 samples and layer
- **Underlying family:** nanomp3 decoder
- **Local input API:** `decode_all::<i16>(&[u8])`
- **Documentation:** [API reference](<https://docs.rs/nanomp3/0.2.0/nanomp3/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3/parsers.json) · [control verification](../../../../data/rust/mp3/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "layer": 3,
  "sample_rate": 8000,
  "samples": 8000
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/rust/nanomp3/README.md)

```sh
python3 parsarium.py build mp3 rust nanomp3
python3 parsarium.py run mp3 rust nanomp3 controls/mp3/id3v2-tagged-tone.mp3
```
