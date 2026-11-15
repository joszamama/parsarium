# mpl-simple-svg-parser — SVG / Python

- **Pinned release:** `0.2.1`
- **License:** BSD-3-Clause
- **Parsed scope:** SVG paths for Matplotlib
- **Underlying family:** CairoSVG and picosvg conversion plus svgpath2mpl
- **Local input API:** `SVGMplPathIterator(local_svg_bytes).iter_path_attrib()`
- **Documentation:** [API reference](<https://leejjoon.github.io/jjl-mpl-blog/posts/mpl-20241027-mpl-simple-svg-parser-user-guide/index.html>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "viewbox": [
    0,
    0,
    2,
    1
  ],
  "paths": 2
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
