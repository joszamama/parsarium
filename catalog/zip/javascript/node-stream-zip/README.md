# node-stream-zip — ZIP / JavaScript

- **Pinned release:** `1.16.0`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** node-stream-zip
- **Local input API:** `new StreamZip.async({file:path}); entries(); entryData(name)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/node-stream-zip>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/javascript/node_stream_zip/README.md)

```sh
python3 parsarium.py build zip javascript node_stream_zip
python3 parsarium.py run zip javascript node_stream_zip controls/zip/hello.zip
```
