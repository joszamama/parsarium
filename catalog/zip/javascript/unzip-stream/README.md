# unzip-stream — ZIP / JavaScript

- **Pinned release:** `0.3.4`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** unzip-stream
- **Local input API:** `Readable.pipe(unzip.Parse()); async iterate entries`
- **Documentation:** [API reference](<https://www.npmjs.com/package/unzip-stream>)
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

Based on unzip and unzipper, but documents a new streaming engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
