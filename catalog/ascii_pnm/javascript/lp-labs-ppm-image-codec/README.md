# @lp-labs/ppm-image-codec — ASCII PNM / JavaScript

- **Pinned release:** `0.1.0`
- **License:** MIT
- **Parsed scope:** P3 RGB pixels and dimensions
- **Underlying family:** lp-labs PPM decoder
- **Local input API:** `decodePpm(localUint8Array)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@lp-labs/ppm-image-codec>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_pnm/parsers.json) · [control verification](../../../../data/javascript/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "maxval": 255,
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/javascript/lp_labs_ppm_image_codec/README.md)

```sh
python3 parsarium.py build ascii_pnm javascript lp_labs_ppm_image_codec
python3 parsarium.py run ascii_pnm javascript lp_labs_ppm_image_codec controls/ascii_pnm/red-green.ppm
```
