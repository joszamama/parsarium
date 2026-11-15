# vsd-mp4 — MP4 / Rust

- **Pinned release:** `0.2.1`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** MP4 movie header timescale
- **Underlying family:** Shaka Player MP4 parser port
- **Local input API:** `Mp4Parser::base_box("moov", children).full_box("mvhd", callback).parse(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/vsd-mp4/0.2.1/vsd_mp4/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "movie_timescale": 8000
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
