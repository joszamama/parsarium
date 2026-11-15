# lofty — MP4 / Rust

- **Pinned release:** `0.25.5`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** MP4 title metadata
- **Underlying family:** Lofty MP4 metadata parser
- **Local input API:** `read_from_path(path).primary_tag().title()`
- **Documentation:** [API reference](<https://docs.rs/lofty/0.25.5/lofty/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
