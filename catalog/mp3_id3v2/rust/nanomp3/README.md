# nanomp3 — MP3 with ID3v2 / Rust

- **Pinned release:** `0.2.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** Decoded MP3 samples and layer
- **Underlying family:** nanomp3 decoder
- **Local input API:** `decode_all::<i16>(&[u8])`
- **Documentation:** [API reference](<https://docs.rs/nanomp3/0.2.0/nanomp3/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3_id3v2/parsers.json) · [control verification](../../../../data/rust/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "layer": 3,
  "sample_rate": 8000,
  "samples": 8000
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
