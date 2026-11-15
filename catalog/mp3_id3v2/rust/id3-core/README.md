# id3-core — MP3 with ID3v2 / Rust

- **Pinned release:** `0.3.1`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** ID3v2 version, title, artist
- **Underlying family:** id3-core tag parser
- **Local input API:** `Tag::parse(&[u8]).text_field()`
- **Documentation:** [API reference](<https://docs.rs/id3-core/0.3.1/id3_core/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3_id3v2/parsers.json) · [control verification](../../../../data/rust/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "version": 3,
  "title": "Parsarium",
  "artist": "Control"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
