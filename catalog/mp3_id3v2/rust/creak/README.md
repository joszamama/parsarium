# creak — MP3 with ID3v2 / Rust

- **Pinned release:** `0.3.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** MP3 audio header and first decoded sample
- **Underlying family:** minimp3 C decoder
- **Local input API:** `Decoder::open(path).info()/into_samples()`
- **Documentation:** [API reference](<https://docs.rs/creak/0.3.0/creak/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3_id3v2/parsers.json) · [control verification](../../../../data/rust/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "first_sample": 0.0
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
