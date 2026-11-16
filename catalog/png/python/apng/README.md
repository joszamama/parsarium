# apng — PNG / Python

- **Pinned release:** `0.3.4`
- **License:** MIT
- **Parsed scope:** chunks and dimensions
- **Underlying family:** pyAPNG chunk parser
- **Local input API:** `apng.PNG.open(local path)`
- **Documentation:** [API reference](<https://pypi.org/project/apng/0.3.4/>)
- **Catalog evidence:** [parser record](../../../../data/python/png/parsers.json) · [control verification](../../../../data/python/png/verification.json) · [within-ecosystem ranking](../../../../data/python/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "chunks": [
    "IHDR",
    "IDAT",
    "IEND"
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
