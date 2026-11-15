# ijp-imageio — ASCII PNM / Java

- **Pinned release:** `2.3.1`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** ASCII P3 PPM dimensions and red/green pixels
- **Underlying family:** IJ Plugins ImageIO wrapper over JAI PNM ImageIO provider
- **Local input API:** `IJImageIO.read(File localPpm) with installed JAI ImageIO PNM provider`
- **Documentation:** [API reference](<https://github.com/ij-plugins/ijp-imageio/blob/master/src/main/java/ij_plugins/imageio/IJImageIO.java>)
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
