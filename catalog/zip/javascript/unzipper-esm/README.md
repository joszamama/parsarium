# unzipper-esm — ZIP / JavaScript

- **Pinned release:** `0.13.3`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** unzipper
- **Local input API:** `Open.buffer(Buffer); entry.buffer()`
- **Documentation:** [API reference](<https://github.com/catamphetamine/node-unzipper>)
- **Catalog evidence:** [parser record](../../../../data/javascript/zip/parsers.json) · [control verification](../../../../data/javascript/zip/verification.json) · [within-ecosystem ranking](../../../../data/javascript/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "entries": [
    "hello.txt"
  ],
  "content": "parsarium\n"
}
```

ES module fork of unzipper.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
