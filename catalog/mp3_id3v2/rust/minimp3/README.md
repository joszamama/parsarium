# minimp3 — MP3 with ID3v2 / Rust

- **Pinned release:** `0.6.1`
- **License:** MIT
- **Parsed scope:** Decoded first MPEG Layer III frame
- **Underlying family:** minimp3 C decoder
- **Local input API:** `Decoder::new(File).next_frame()`
- **Documentation:** [API reference](<https://docs.rs/minimp3/0.6.1/minimp3/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3_id3v2/parsers.json) · [control verification](../../../../data/rust/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "decoded_samples": 576
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/rust/minimp3/README.md)

```sh
python3 parsarium.py build mp3_id3v2 rust minimp3
python3 parsarium.py run mp3_id3v2 rust minimp3 controls/mp3_id3v2/tone-tags.mp3
```
