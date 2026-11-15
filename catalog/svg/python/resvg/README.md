# resvg — SVG / Python

- **Pinned release:** `0.2.0`
- **License:** MIT
- **Parsed scope:** SVG tree and intrinsic dimensions
- **Underlying family:** Rust resvg/usvg through resvg-py binding
- **Local input API:** `resvg.usvg.Tree.from_str(local_svg_text, resvg.usvg.Options.default())`
- **Documentation:** [API reference](<https://pypi.org/project/resvg/0.2.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "size": [
    2,
    1
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
