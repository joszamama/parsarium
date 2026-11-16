# svgr — SVG / Rust

- **Pinned release:** `0.50.2`
- **License:** MPL-2.0
- **Parsed scope:** SVG raster rendering
- **Underlying family:** usvgr fork of usvg lineage
- **Local input API:** `usvgr::Tree::from_data(&bytes, &Options::default()); render(&tree, transform, pixmap, cache, pool, context)`
- **Documentation:** [API reference](<https://docs.rs/svgr/0.50.2/svgr/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2.0,
  "height": 1.0,
  "rgba": [
    255,
    0,
    0,
    255,
    0,
    255,
    0,
    255
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/rust/svgr/README.md)

```sh
python3 parsarium.py build svg rust svgr
python3 parsarium.py run svg rust svgr controls/svg/red-green.svg
```
