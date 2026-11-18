# imageio — ASCII PNM / Python

- **Pinned release:** `2.38.1`
- **Upstream:** [source repository](<https://github.com/imageio/imageio>) · [PyPI](<https://pypi.org/project/imageio/>)
- **License:** BSD-2-Clause
- **Parsed scope:** P3 pixels
- **Underlying family:** ImageIO via Pillow PPM
- **Local input API:** `imageio.v3.imread(local path)`
- **Documentation:** [API reference](<https://imageio.readthedocs.io/en/stable/reference/userapi.html>)
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/python/imageio/README.md)

```sh
python3 parsarium.py build ascii_pnm python imageio
python3 parsarium.py run ascii_pnm python imageio controls/ascii_pnm/red-green.ppm
```
