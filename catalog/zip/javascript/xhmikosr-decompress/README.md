# @xhmikosr/decompress — ZIP / JavaScript

- **Pinned release:** `11.1.4`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** yauzl
- **Local input API:** `decompress(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@xhmikosr/decompress>)
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

Uses @xhmikosr/decompress-unzip, which uses yauzl.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
