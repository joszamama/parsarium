# svgcleaner — SVG / Rust

- **Pinned release:** `0.9.5`
- **License:** GPL-2.0
- **Parsed scope:** SVG DOM elements before cleaning
- **Underlying family:** svgdom 0.10.5
- **Local input API:** `cleaner::parse_data(svg_text, &ParseOptions::default())`
- **Documentation:** [API reference](<https://docs.rs/svgcleaner/0.9.5/svgcleaner/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "rects": 2,
  "has_svg": true
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/rust/svgcleaner/README.md)

```sh
python3 parsarium.py build svg rust svgcleaner
python3 parsarium.py run svg rust svgcleaner controls/svg/red-green.svg
```
