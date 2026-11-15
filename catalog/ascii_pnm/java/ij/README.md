# ij — ASCII PNM / Java

- **Pinned release:** `1.54p`
- **License:** Public domain
- **Parsed scope:** ASCII PPM dimensions and red/green pixels
- **Underlying family:** ImageJ PGM/PPM reader
- **Local input API:** `ij.io.Opener.openImage(String local path).getBufferedImage()`
- **Documentation:** [API reference](<https://imagej.net/ij/developer/api/ij/ij/plugin/PGM_Reader.html>)
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
