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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
