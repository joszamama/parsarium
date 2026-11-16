# purejsimage — ASCII PNM / JavaScript

- **Pinned release:** `0.17.0`
- **License:** MIT
- **Parsed scope:** P3 parsed format metadata and dimensions
- **Underlying family:** PureJsImage Netpbm codec
- **Local input API:** `createImageLibrary({codecs:[netpbmCodec]}).open(localPath).metadata()`
- **Documentation:** [API reference](<https://www.npmjs.com/package/purejsimage>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_pnm/parsers.json) · [control verification](../../../../data/javascript/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "format": "netpbm",
  "variant": "P3",
  "width": 2,
  "height": 1,
  "channels": 3
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/javascript/purejsimage/README.md)

```sh
python3 parsarium.py build ascii_pnm javascript purejsimage
python3 parsarium.py run ascii_pnm javascript purejsimage controls/ascii_pnm/red-green.ppm
```
