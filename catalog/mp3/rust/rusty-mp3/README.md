# rusty_mp3 — MP3 / Rust

- **Pinned release:** `1.0.5`
- **License:** Apache-2.0
- **Parsed scope:** Decoded first MPEG Layer III frame
- **Underlying family:** rusty_mp3 decoder
- **Local input API:** `Mp3Decoder::new().push(&[u8]).next_frame()`
- **Documentation:** [API reference](<https://docs.rs/rusty_mp3/1.0.5/rusty_mp3/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3/parsers.json) · [control verification](../../../../data/rust/mp3/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "decoded_samples": 576
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/rust/rusty_mp3/README.md)

```sh
python3 parsarium.py build mp3 rust rusty_mp3
python3 parsarium.py run mp3 rust rusty_mp3 controls/mp3/id3v2-tagged-tone.mp3
```
