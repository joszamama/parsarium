# yauzl — ZIP / JavaScript

- **Pinned release:** `3.4.0`
- **Upstream:** [source repository](<https://github.com/thejoshwolfe/yauzl>) · [npm](<https://www.npmjs.com/package/yauzl>)
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** yauzl
- **Local input API:** `fromBufferPromise(Buffer); eachEntry(); openReadStreamPromise(entry)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/yauzl>)
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

[Docker harness and verification receipt](../../../../projects/zip/javascript/yauzl/README.md)

```sh
python3 parsarium.py build zip javascript yauzl
python3 parsarium.py run zip javascript yauzl controls/zip/hello.zip
```
