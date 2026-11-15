# byteparse — PNG / Python

- **Pinned release:** `0.1.0`
- **License:** MIT
- **Parsed scope:** IHDR dimensions
- **Underlying family:** byteparse PNG grammar
- **Local input API:** `byteparse.formats.PNGFile.parse(local bytes)`
- **Documentation:** [API reference](<https://pypi.org/project/byteparse/0.1.0/>)
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

[Docker harness and verification receipt](../../../../projects/png/python/byteparse/README.md)

```sh
python3 parsarium.py build png python byteparse
python3 parsarium.py run png python byteparse controls/png/red-green.png
```
