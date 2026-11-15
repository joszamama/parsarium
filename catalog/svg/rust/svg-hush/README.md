# svg-hush — SVG / Rust

- **Pinned release:** `0.9.7`
- **License:** Apache-2.0 OR MIT
- **Parsed scope:** SVG-aware stream filtering
- **Underlying family:** svg-hush SVG filter
- **Local input API:** `Filter::new().filter(&mut input_bytes, &mut output_bytes)`
- **Documentation:** [API reference](<https://docs.rs/svg-hush/0.9.7/svg_hush/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "rects_retained": 2,
  "svg_retained": true
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
