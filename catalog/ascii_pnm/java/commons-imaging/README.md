# commons-imaging — ASCII PNM / Java

- **Pinned release:** `1.0.0-alpha6`
- **License:** Apache-2.0
- **Parsed scope:** ASCII PPM dimensions and red/green pixels
- **Underlying family:** Apache Commons Imaging PNM decoder
- **Local input API:** `Imaging.getBufferedImage(File)`
- **Documentation:** [API reference](<https://commons.apache.org/proper/commons-imaging/formatsupport.html>)
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
