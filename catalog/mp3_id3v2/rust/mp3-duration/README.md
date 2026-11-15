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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
