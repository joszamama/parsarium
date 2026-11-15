# rff-format-mp4 — MP4 / Rust

- **Pinned release:** `0.4.6`
- **License:** Apache-2.0
- **Parsed scope:** MP4 audio and video streams
- **Underlying family:** RFF MP4 demuxer
- **Local input API:** `register(FormatRegistry); open_demuxer("mp4", File).read_header()`
- **Documentation:** [API reference](<https://docs.rs/rff-format-mp4/0.4.6/rff_format_mp4/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "streams": 2
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
