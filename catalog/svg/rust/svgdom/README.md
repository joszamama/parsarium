# svgdom — SVG / Rust

- **Pinned release:** `0.18.0`
- **License:** MIT/Apache-2.0
- **Parsed scope:** SVG DOM elements
- **Underlying family:** svgdom + svgtypes lineage
- **Local input API:** `Document::from_str(svg_text).svg_element()/descendants()`
- **Documentation:** [API reference](<https://docs.rs/svgdom/0.18.0/svgdom/>)
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

[Docker harness and verification receipt](../../../../projects/svg/rust/svgdom/README.md)

```sh
python3 parsarium.py build svg rust svgdom
python3 parsarium.py run svg rust svgdom controls/svg/red-green.svg
```
