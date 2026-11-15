# skia-python — SVG / Python

- **Pinned release:** `144.1`
- **License:** BSD-3-Clause
- **Parsed scope:** SVG DOM and intrinsic dimensions
- **Underlying family:** Skia SVGDOM binding
- **Local input API:** `skia.SVGDOM.MakeFromStream(skia.MemoryStream.MakeCopy(local_svg_bytes))`
- **Documentation:** [API reference](<https://github.com/skia-python/skia-python/blob/main/src/skia/SVGDOM.cpp>)
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
