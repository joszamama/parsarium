# nsvg — SVG / Rust

- **Pinned release:** `0.5.1`
- **License:** Zlib/MIT
- **Parsed scope:** SVG image dimensions via NanoSVG
- **Underlying family:** NanoSVG C parser
- **Local input API:** `SvgImage::parse_file(path, Units::Pixel, 96.0)`
- **Documentation:** [API reference](<https://docs.rs/nsvg/0.5.1/nsvg/>)
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

[Docker harness and verification receipt](../../../../projects/svg/rust/nsvg/README.md)

```sh
python3 parsarium.py build svg rust nsvg
python3 parsarium.py run svg rust nsvg controls/svg/red-green.svg
```
