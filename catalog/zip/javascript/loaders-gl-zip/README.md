# @loaders.gl/zip — ZIP / JavaScript

- **Pinned release:** `4.5.4`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** JSZip
- **Local input API:** `ZipLoader.parse(ArrayBuffer)`
- **Documentation:** [API reference](<https://loaders.gl/docs/modules/zip/api-reference/zip-loader>)
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

The ZIP loader wraps JSZip.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
