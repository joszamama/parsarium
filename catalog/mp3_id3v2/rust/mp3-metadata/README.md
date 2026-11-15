# mp3-metadata — MP3 with ID3v2 / Rust

- **Pinned release:** `0.4.0`
- **License:** MIT
- **Parsed scope:** MPEG frame count and sample rate
- **Underlying family:** mp3-metadata parser
- **Local input API:** `read_from_file(path)`
- **Documentation:** [API reference](<https://docs.rs/mp3-metadata/0.4.0/mp3_metadata/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3_id3v2/parsers.json) · [control verification](../../../../data/rust/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "frames": 17,
  "sample_rate": 8000
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
