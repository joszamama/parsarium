# moosicbox_audiotags — MP3 with ID3v2 / Rust

- **Pinned release:** `0.1.0`
- **License:** MIT
- **Parsed scope:** ID3v2 title and artist
- **Underlying family:** moosicbox_audiotags via id3
- **Local input API:** `Tag::new().read_from_path(path)`
- **Documentation:** [API reference](<https://docs.rs/moosicbox_audiotags/0.1.0/moosicbox_audiotags/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp3_id3v2/parsers.json) · [control verification](../../../../data/rust/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
