# pngtools — PNG / Python

- **Pinned release:** `1.0.2`
- **License:** MIT
- **Parsed scope:** chunks
- **Underlying family:** pngtools chunk parser
- **Local input API:** `pngtools.read_file(local path); get_type_of_chunk`
- **Documentation:** [API reference](<https://github.com/its-just-nans/pngtools/blob/main/pngtools/lib.py>)
- **Catalog evidence:** [parser record](../../../../data/python/png/parsers.json) · [control verification](../../../../data/python/png/verification.json) · [within-ecosystem ranking](../../../../data/python/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "chunks": [
    "IHDR",
    "IDAT",
    "IEND"
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
