# OpenImageIO — ASCII PNM / Python

- **Pinned release:** `3.2.2.0`
- **License:** Apache-2.0
- **Parsed scope:** P3 pixels
- **Underlying family:** OpenImageIO PNM
- **Local input API:** `OpenImageIO.ImageInput.open(local path); read_image()`
- **Documentation:** [API reference](<https://openimageio.readthedocs.io/en/v3.2.1.0/pythonbindings.html>)
- **Catalog evidence:** [parser record](../../../../data/python/ascii_pnm/parsers.json) · [control verification](../../../../data/python/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/python/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgb0": [
    255,
    0,
    0
  ],
  "rgb1": [
    0,
    255,
    0
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/python/openimageio/README.md)

```sh
python3 parsarium.py build ascii_pnm python openimageio
python3 parsarium.py run ascii_pnm python openimageio controls/ascii_pnm/red-green.ppm
```
