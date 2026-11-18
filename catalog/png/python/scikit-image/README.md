# scikit-image — PNG / Python

- **Pinned release:** `0.26.0`
- **Upstream:** [source repository](<https://github.com/scikit-image/scikit-image>) · [PyPI](<https://pypi.org/project/scikit-image/>)
- **License:** BSD-3-Clause
- **Parsed scope:** pixels
- **Underlying family:** scikit-image via ImageIO/Pillow
- **Local input API:** `skimage.io.imread(local path)`
- **Documentation:** [API reference](<https://scikit-image.org/docs/0.26.x/api/skimage.io.html>)
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

[Docker harness and verification receipt](../../../../projects/png/python/scikit_image/README.md)

```sh
python3 parsarium.py build png python scikit_image
python3 parsarium.py run png python scikit_image controls/png/red-green.png
```
