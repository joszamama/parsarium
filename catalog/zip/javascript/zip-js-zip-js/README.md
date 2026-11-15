# @zip.js/zip.js — ZIP / JavaScript

- **Pinned release:** `2.24.0`
- **License:** BSD-3-Clause
- **Parsed scope:** entries_and_content
- **Underlying family:** zip.js
- **Local input API:** `new ZipReader(new Uint8ArrayReader(bytes)); getEntries(); entry.getData(new TextWriter())`
- **Documentation:** [API reference](<https://gildas-lormeau.github.io/zip.js/api/classes/ZipReader.html>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
