# lofty — MP4 / Rust

- **Pinned release:** `0.25.5`
- **Upstream:** [source repository](<https://github.com/Serial-ATA/lofty-rs>) · [crates.io](<https://crates.io/crates/lofty>)
- **License:** MIT OR Apache-2.0
- **Parsed scope:** MP4 title metadata
- **Underlying family:** Lofty MP4 metadata parser
- **Local input API:** `read_from_path(path).primary_tag().title()`
- **Documentation:** [API reference](<https://docs.rs/lofty/0.25.5/lofty/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/rust/lofty/README.md)

```sh
python3 parsarium.py build mp4 rust lofty
python3 parsarium.py run mp4 rust lofty controls/mp4/red-av.mp4
```
