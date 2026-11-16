# Willow — PNG / Python

- **Pinned release:** `1.12.0`
- **License:** BSD-3-Clause
- **Parsed scope:** dimensions
- **Underlying family:** Willow via Pillow
- **Local input API:** `willow.image.Image.open(local stream).get_size()`
- **Documentation:** [API reference](<https://pypi.org/project/Willow/1.12.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/png/parsers.json) · [control verification](../../../../data/python/png/verification.json) · [within-ecosystem ranking](../../../../data/python/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

Observed or documented wrapper path; this package is counted as a distinct API package, not an independent PNG engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/png/python/willow/README.md)

```sh
python3 parsarium.py build png python willow
python3 parsarium.py run png python willow controls/png/red-green.png
```
