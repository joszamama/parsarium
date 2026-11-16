# zip-lib — ZIP / JavaScript

- **Pinned release:** `1.4.0`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** yauzl
- **Local input API:** `extract(Buffer, targetFolder)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/zip-lib>)
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

The pinned release depends on yauzl@^3.4.0.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/javascript/zip_lib/README.md)

```sh
python3 parsarium.py build zip javascript zip_lib
python3 parsarium.py run zip javascript zip_lib controls/zip/hello.zip
```
