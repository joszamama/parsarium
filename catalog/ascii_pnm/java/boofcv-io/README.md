# boofcv-io — ASCII PNM / Java

- **Pinned release:** `1.6.0`
- **License:** Apache-2.0
- **Parsed scope:** ASCII PPM dimensions and red/green pixels
- **Underlying family:** BoofCV ImageIO wrapper over PNM provider (TwelveMonkeys or JAI)
- **Local input API:** `UtilImageIO.loadImage(String local path) with installed PNM ImageIO provider`
- **Documentation:** [API reference](<https://boofcv.org/javadoc/boofcv/io/image/UtilImageIO.html>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_pnm/parsers.json) · [control verification](../../../../data/java/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

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
