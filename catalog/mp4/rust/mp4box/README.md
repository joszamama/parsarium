# mp4box — MP4 / Rust

- **Pinned release:** `0.14.0`
- **License:** MIT
- **Parsed scope:** Decoded MP4 top-level box tree
- **Underlying family:** mp4box parser
- **Local input API:** `get_boxes(&mut File, len, true)`
- **Documentation:** [API reference](<https://docs.rs/mp4box/0.14.0/mp4box/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "top_boxes": 4,
  "has_moov": true
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/rust/mp4box/README.md)

```sh
python3 parsarium.py build mp4 rust mp4box
python3 parsarium.py run mp4 rust mp4box controls/mp4/red-av.mp4
```
