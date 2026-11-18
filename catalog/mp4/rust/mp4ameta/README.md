# mp4ameta — MP4 / Rust

- **Pinned release:** `0.13.0`
- **Upstream:** [source repository](<https://github.com/saecki/mp4ameta>) · [crates.io](<https://crates.io/crates/mp4ameta>)
- **License:** MIT OR Apache-2.0
- **Parsed scope:** MP4 title metadata
- **Underlying family:** mp4ameta iTunes atom parser
- **Local input API:** `Tag::read_from_path(path).title()`
- **Documentation:** [API reference](<https://docs.rs/mp4ameta/0.13.0/mp4ameta/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/rust/mp4ameta/README.md)

```sh
python3 parsarium.py build mp4 rust mp4ameta
python3 parsarium.py run mp4 rust mp4ameta controls/mp4/red-av.mp4
```
