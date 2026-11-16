# re_mp4 — MP4 / Rust

- **Pinned release:** `0.5.1`
- **License:** MIT
- **Parsed scope:** MP4 movie track table
- **Underlying family:** mp4-rs-derived Rerun parser
- **Local input API:** `Mp4::read_file(path).tracks()`
- **Documentation:** [API reference](<https://docs.rs/re_mp4/0.5.1/re_mp4/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "tracks": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/rust/re_mp4/README.md)

```sh
python3 parsarium.py build mp4 rust re_mp4
python3 parsarium.py run mp4 rust re_mp4 controls/mp4/red-av.mp4
```
