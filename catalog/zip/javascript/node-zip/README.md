# node-zip — ZIP / JavaScript

- **Pinned release:** `1.1.1`
- **License:** MIT (package README; registry metadata omits license)
- **Parsed scope:** entries_and_content
- **Underlying family:** JSZip
- **Local input API:** `new NodeZip(Buffer, {base64:false}); zip.file(name).asText()`
- **Documentation:** [API reference](<https://www.npmjs.com/package/node-zip>)
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

The pinned release depends on jszip@2.5.0.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
