# mp4san — MP4 / Rust

- **Pinned release:** `0.5.4`
- **Upstream:** [source repository](<https://github.com/signalapp/mp4san>) · [crates.io](<https://crates.io/crates/mp4san>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/rust/mp4san/README.md)

```sh
python3 parsarium.py build mp4 rust mp4san
python3 parsarium.py run mp4 rust mp4san controls/mp4/red-av.mp4
```
