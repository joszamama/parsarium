# yauzl-promise — ZIP / JavaScript

- **Pinned release:** `4.0.0`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** yauzl-promise
- **Local input API:** `fromBuffer(Buffer); async iterate entries; entry.openReadStream()`
- **Documentation:** [API reference](<https://www.npmjs.com/package/yauzl-promise>)
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

Version 4 is a rewrite rather than a wrapper of yauzl.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/javascript/yauzl_promise/README.md)

```sh
python3 parsarium.py build zip javascript yauzl_promise
python3 parsarium.py run zip javascript yauzl_promise controls/zip/hello.zip
```
