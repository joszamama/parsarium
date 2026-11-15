# shiguredo_mp4 — MP4 / Rust

- **Pinned release:** `2026.6.0-canary.2`
- **License:** Apache-2.0
- **Parsed scope:** Typed MP4 top-level boxes
- **Underlying family:** Shiguredo MP4 parser
- **Local input API:** `Mp4File::decode(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/shiguredo_mp4/2026.6.0-canary.2/shiguredo_mp4/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "top_boxes": 4,
  "consumed_bytes": 2670
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
