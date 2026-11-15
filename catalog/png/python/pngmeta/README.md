# pngmeta — PNG / Python

- **Pinned release:** `0.2.1`
- **License:** Unlicense
- **Parsed scope:** tEXt metadata
- **Underlying family:** pngmeta chunk parser
- **Local input API:** `pngmeta.PngMeta(local path).get("Title")`
- **Documentation:** [API reference](<https://pypi.org/project/pngmeta/0.2.1/>)
- **Catalog evidence:** [parser record](../../../../data/python/png/parsers.json) · [control verification](../../../../data/python/png/verification.json) · [within-ecosystem ranking](../../../../data/python/png/ranking.md)
- **Valid control:** [`controls/png/red-green-title.png`](../../../../controls/png/red-green-title.png)

## Observed control result

```json
{
  "title": "Parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/python/pngmeta/README.md)

```sh
python3 parsarium.py build png python pngmeta
python3 parsarium.py run png python pngmeta controls/png/red-green-title.png
```
