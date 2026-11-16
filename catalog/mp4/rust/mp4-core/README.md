# mp4-core — MP4 / Rust

- **Pinned release:** `0.3.2`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** MP4 file type, movie header, and tracks
- **Underlying family:** mp4-core box parser
- **Local input API:** `Mp4File::parse(&bytes).tracks`
- **Documentation:** [API reference](<https://docs.rs/mp4-core/0.3.2/mp4_core/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/rust/mp4_core/README.md)

```sh
python3 parsarium.py build mp4 rust mp4_core
python3 parsarium.py run mp4 rust mp4_core controls/mp4/red-av.mp4
```
