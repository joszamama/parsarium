# pypng — PNG / Python

- **Pinned release:** `0.20220715.0`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** PyPNG
- **Local input API:** `png.Reader(filename=local path).asRGBA8()`
- **Documentation:** [API reference](<https://drj11.gitlab.io/pypng/png.html>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/png/python/pypng/README.md)

```sh
python3 parsarium.py build png python pypng
python3 parsarium.py run png python pypng controls/png/red-green.png
```
