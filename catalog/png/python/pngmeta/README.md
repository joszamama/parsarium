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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
