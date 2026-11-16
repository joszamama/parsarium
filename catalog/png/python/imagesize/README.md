# imagesize — PNG / Python

- **Pinned release:** `2.0.1`
- **License:** MIT
- **Parsed scope:** dimensions
- **Underlying family:** imagesize PNG header
- **Local input API:** `imagesize.get(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/imagesize/2.0.1/>)
- **Catalog evidence:** [parser record](../../../../data/python/png/parsers.json) · [control verification](../../../../data/python/png/verification.json) · [within-ecosystem ranking](../../../../data/python/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/python/imagesize/README.md)

```sh
python3 parsarium.py build png python imagesize
python3 parsarium.py run png python imagesize controls/png/red-green.png
```
