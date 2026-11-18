# fflate — ZIP / JavaScript

- **Pinned release:** `0.8.3`
- **Upstream:** [source repository](<https://github.com/101arrowz/fflate>) · [npm](<https://www.npmjs.com/package/fflate>)
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** fflate
- **Local input API:** `unzipSync(Uint8Array)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/fflate>)
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

[Docker harness and verification receipt](../../../../projects/zip/javascript/fflate/README.md)

```sh
python3 parsarium.py build zip javascript fflate
python3 parsarium.py run zip javascript fflate controls/zip/hello.zip
```
