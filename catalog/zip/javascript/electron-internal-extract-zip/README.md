# @electron-internal/extract-zip — ZIP / JavaScript

- **Pinned release:** `1.0.8`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** Electron native ZIP extractor
- **Local input API:** `extract(localZipPath, {dir})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@electron-internal/extract-zip>)
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

Native implementation; exact underlying parser library has not been established.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
