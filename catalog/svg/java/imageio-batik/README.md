# imageio-batik — SVG / Java

- **Pinned release:** `3.15.2`
- **License:** BSD-3-Clause
- **Parsed scope:** Rendered SVG pixels
- **Underlying family:** TwelveMonkeys ImageIO wrapper over Apache Batik
- **Local input API:** `TwelveMonkeys SVG ImageReader.setInput(ImageInputStream); read(0)`
- **Documentation:** [API reference](<https://github.com/haraldk/TwelveMonkeys#file-formats-supported>)
- **Catalog evidence:** [parser record](../../../../data/java/svg/parsers.json) · [control verification](../../../../data/java/svg/verification.json) · [within-ecosystem ranking](../../../../data/java/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
