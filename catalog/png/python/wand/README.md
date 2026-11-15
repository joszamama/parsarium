# Wand — PNG / Python

- **Pinned release:** `0.7.2`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** ImageMagick
- **Local input API:** `wand.image.Image(filename=local path).export_pixels`
- **Documentation:** [API reference](<https://docs.wand-py.org/en/latest/guide/read.html>)
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

[Docker harness and verification receipt](../../../../projects/png/python/wand/README.md)

```sh
python3 parsarium.py build png python wand
python3 parsarium.py run png python wand controls/png/red-green.png
```
