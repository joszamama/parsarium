# mp4-track — MP4 / Rust

- **Pinned release:** `0.1.0`
- **License:** MIT
- **Parsed scope:** MP4 movie track table
- **Underlying family:** mp4-track parser
- **Local input API:** `Mp4Reader::open(File).tracks()`
- **Documentation:** [API reference](<https://docs.rs/mp4-track/0.1.0/mp4_track/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/rust/mp4_track/README.md)

```sh
python3 parsarium.py build mp4 rust mp4_track
python3 parsarium.py run mp4 rust mp4_track controls/mp4/red-av.mp4
```
