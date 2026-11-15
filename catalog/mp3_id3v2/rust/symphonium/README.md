# symphonium — MP3 with ID3v2 / Rust

- **Pinned release:** `0.13.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** MP3 track header
- **Underlying family:** Symphonia MP3 demuxer
- **Local input API:** `probe_from_file(path, None)`
- **Documentation:** [API reference](<https://docs.rs/symphonium/0.13.0/symphonium/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3_id3v2/parsers.json) · [control verification](../../../../data/rust/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
