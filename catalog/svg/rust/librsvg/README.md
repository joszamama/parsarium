# librsvg — SVG / Rust

- **Pinned release:** `2.63.4`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** SVG document loading and intrinsic dimensions
- **Underlying family:** librsvg SVG parser
- **Local input API:** `Loader::new().read_path(path); CairoRenderer::new(&handle).intrinsic_size_in_pixels()`
- **Documentation:** [API reference](<https://docs.rs/librsvg/2.63.4/rsvg/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2.0,
  "height": 1.0
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/rust/librsvg/README.md)

```sh
python3 parsarium.py build svg rust librsvg
python3 parsarium.py run svg rust librsvg controls/svg/red-green.svg
```
