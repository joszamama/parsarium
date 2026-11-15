# png-chunks-extract — PNG / JavaScript

- **Pinned release:** `1.0.0`
- **License:** MIT
- **Parsed scope:** chunks
- **Underlying family:** png-chunks-extract
- **Local input API:** `extract(Buffer)`
- **Documentation:** [API reference](<https://github.com/hughsk/png-chunks-extract/blob/master/README.md>)
- **Catalog evidence:** [parser record](../../../../data/javascript/png/parsers.json) · [control verification](../../../../data/javascript/png/verification.json) · [within-ecosystem ranking](../../../../data/javascript/png/ranking.md)
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

Parses PNG chunk structure only; does not decode pixels.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
