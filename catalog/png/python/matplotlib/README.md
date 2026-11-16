# matplotlib — PNG / Python

- **Pinned release:** `3.11.2`
- **License:** Matplotlib License 1.3
- **Parsed scope:** pixels
- **Underlying family:** Matplotlib via Pillow
- **Local input API:** `matplotlib.image.imread(local path)`
- **Documentation:** [API reference](<https://matplotlib.org/stable/api/image_api.html>)
- **Catalog evidence:** [parser record](../../../../data/python/png/parsers.json) · [control verification](../../../../data/python/png/verification.json) · [within-ecosystem ranking](../../../../data/python/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgba0": [
    255,
    0,
    0,
    255
  ],
  "rgba1": [
    0,
    255,
    0,
    255
  ]
}
```

Observed or documented wrapper path; this package is counted as a distinct API package, not an independent PNG engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/python/matplotlib/README.md)

```sh
python3 parsarium.py build png python matplotlib
python3 parsarium.py run png python matplotlib controls/png/red-green.png
```
