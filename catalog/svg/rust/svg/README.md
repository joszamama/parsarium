# svg — SVG / Rust

- **Pinned release:** `0.18.0`
- **Upstream:** [source repository](<https://github.com/bodoni/svg>) · [crates.io](<https://crates.io/crates/svg>)
- **License:** Apache-2.0 OR MIT
- **Parsed scope:** SVG element event parsing
- **Underlying family:** svg crate parser
- **Local input API:** `open(path, &mut content) -> Parser<Event::Tag>`
- **Documentation:** [API reference](<https://docs.rs/svg/0.18.0/svg/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "rects": 2,
  "paths": 0
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/rust/svg/README.md)

```sh
python3 parsarium.py build svg rust svg
python3 parsarium.py run svg rust svg controls/svg/red-green.svg
```
