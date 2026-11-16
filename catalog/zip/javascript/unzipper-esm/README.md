# unzipper-esm — ZIP / JavaScript

- **Pinned release:** `0.13.3`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** unzipper
- **Local input API:** `Open.buffer(Buffer); entry.buffer()`
- **Documentation:** [API reference](<https://github.com/catamphetamine/node-unzipper>)
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

ES module fork of unzipper.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/javascript/unzipper_esm/README.md)

```sh
python3 parsarium.py build zip javascript unzipper_esm
python3 parsarium.py run zip javascript unzipper_esm controls/zip/hello.zip
```
