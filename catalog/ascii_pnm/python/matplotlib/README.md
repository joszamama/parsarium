# matplotlib — ASCII PNM / Python

- **Pinned release:** `3.11.2`
- **License:** Matplotlib License 1.3
- **Parsed scope:** P3 pixels
- **Underlying family:** Matplotlib via Pillow PPM
- **Local input API:** `matplotlib.image.imread(local path)`
- **Documentation:** [API reference](<https://matplotlib.org/stable/api/image_api.html>)
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/python/matplotlib/README.md)

```sh
python3 parsarium.py build ascii_pnm python matplotlib
python3 parsarium.py run ascii_pnm python matplotlib controls/ascii_pnm/red-green.ppm
```
