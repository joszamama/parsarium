# symphonia-format-isomp4 — MP4 / Rust

- **Pinned release:** `0.6.1`
- **License:** MPL-2.0
- **Parsed scope:** MP4 AAC track and first packet
- **Underlying family:** Symphonia ISO-MP4 demuxer
- **Local input API:** `IsoMp4Reader::try_new(MediaSourceStream).next_packet()`
- **Documentation:** [API reference](<https://docs.rs/symphonia-format-isomp4/0.6.1/symphonia_format_isomp4/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "sample_rate": 8000,
  "packet_bytes": 1129
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
