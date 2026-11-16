# extract-zip — ZIP / JavaScript

- **Pinned release:** `2.0.1`
- **License:** BSD-2-Clause
- **Parsed scope:** entries_and_content
- **Underlying family:** yauzl
- **Local input API:** `extract(localZipPath, {dir, onEntry})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/extract-zip>)
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

This release depends on yauzl@^2.10.0.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
