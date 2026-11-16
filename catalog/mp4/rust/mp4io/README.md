# mp4io — MP4 / Rust

- **Pinned release:** `0.1.2`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** MP4 movie track table
- **Underlying family:** mp4io zero-copy parser
- **Local input API:** `Mp4::parse(&bytes).tracks()`
- **Documentation:** [API reference](<https://docs.rs/mp4io/0.1.2/mp4io/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/rust/mp4io/README.md)

```sh
python3 parsarium.py build mp4 rust mp4io
python3 parsarium.py run mp4 rust mp4io controls/mp4/red-av.mp4
```
