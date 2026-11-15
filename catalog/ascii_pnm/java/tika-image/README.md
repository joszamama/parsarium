# tika-image — ASCII PNM / Java

- **Pinned release:** `4.2.0`
- **License:** Apache-2.0
- **Parsed scope:** ASCII PPM image width and height
- **Underlying family:** Apache Tika ImageParser over ImageIO PNM provider (TwelveMonkeys or JAI)
- **Local input API:** `ImageParser.parse(TikaInputStream local path, ContentHandler, Metadata, ParseContext) with PNM ImageIO provider`
- **Documentation:** [API reference](<https://tika.apache.org/docs/4.0.x/formats.html>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_pnm/parsers.json) · [control verification](../../../../data/java/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
