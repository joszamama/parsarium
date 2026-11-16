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

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/javascript/node_zip/README.md)

```sh
python3 parsarium.py build zip javascript node_zip
python3 parsarium.py run zip javascript node_zip controls/zip/hello.zip
```
