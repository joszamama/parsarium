# mp4-atom — MP4 / Rust

- **Pinned release:** `0.17.1`
- **Upstream:** [source repository](<https://github.com/kixelated/mp4-atom>) · [crates.io](<https://crates.io/crates/mp4-atom>)
- **License:** MIT OR Apache-2.0
- **Parsed scope:** Typed MP4 file-type atom
- **Underlying family:** mp4-atom ISO-BMFF atom parser
- **Local input API:** `Ftyp::read_from(&mut File)`
- **Documentation:** [API reference](<https://docs.rs/mp4-atom/0.17.1/mp4_atom/>)
- **Catalog evidence:** [parser record](../../../../data/rust/mp4/parsers.json) · [control verification](../../../../data/rust/mp4/verification.json) · [within-ecosystem ranking](../../../../data/rust/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "major_brand": "isom",
  "compatible_brands": 4
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/rust/mp4_atom/README.md)

```sh
python3 parsarium.py build mp4 rust mp4_atom
python3 parsarium.py run mp4 rust mp4_atom controls/mp4/red-av.mp4
```
