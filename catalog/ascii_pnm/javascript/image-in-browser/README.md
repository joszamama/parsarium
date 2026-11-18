# image-in-browser — ASCII PNM / JavaScript

- **Pinned release:** `3.7.0`
- **Upstream:** [source repository](<https://github.com/yegor-pelykh/image-in-browser>) · [npm](<https://www.npmjs.com/package/image-in-browser>)
- **License:** MIT
- **Parsed scope:** P3 RGB pixels and dimensions
- **Underlying family:** image-in-browser PNM decoder
- **Local input API:** `decodePnm({data:localUint8Array})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/image-in-browser>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_pnm/parsers.json) · [control verification](../../../../data/javascript/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgb": [
    255,
    0,
    0,
    0,
    255,
    0
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/javascript/image_in_browser/README.md)

```sh
python3 parsarium.py build ascii_pnm javascript image_in_browser
python3 parsarium.py run ascii_pnm javascript image_in_browser controls/ascii_pnm/red-green.ppm
```
