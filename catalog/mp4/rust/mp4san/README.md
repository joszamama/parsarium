# mp4san — MP4 / Rust

- **Pinned release:** `0.5.4`
- **License:** MIT
- **Parsed scope:** MP4 presentation metadata and media-data span
- **Underlying family:** mp4san parser
- **Local input API:** `sanitize(File).data`
- **Documentation:** [API reference](<https://docs.rs/mp4san/0.5.4/mp4san/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "media_data_bytes": 1188
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
