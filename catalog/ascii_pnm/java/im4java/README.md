# im4java — ASCII PNM / Java

- **Pinned release:** `1.4.0`
- **License:** LGPL-2.1
- **Parsed scope:** ASCII P3 PPM format and dimensions
- **Underlying family:** im4java wrapper over host ImageMagick Netpbm decoder
- **Local input API:** `new Info(String localPpmPath,true).getImageFormat()/getImageWidth()/getImageHeight()`
- **Documentation:** [API reference](<https://im4java.sourceforge.net/docs/dev-guide.html>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_pnm/parsers.json) · [control verification](../../../../data/java/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "format": "PPM",
  "width": 2,
  "height": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/java/im4java/README.md)

```sh
python3 parsarium.py build ascii_pnm java im4java
python3 parsarium.py run ascii_pnm java im4java controls/ascii_pnm/red-green.ppm
```
