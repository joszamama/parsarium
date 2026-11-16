# resvglite — SVG / Python

- **Pinned release:** `0.2.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** SVG rendering with dimensions and colored pixels
- **Underlying family:** Rust resvg/usvg vendored binding
- **Local input API:** `resvglite.render_svg(local_svg_bytes, size_px=1)`
- **Documentation:** [API reference](<https://pypi.org/project/resvglite/0.2.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "size": [
    2,
    1
  ],
  "red": [
    255,
    0,
    0,
    255
  ],
  "green": [
    0,
    255,
    0,
    255
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
