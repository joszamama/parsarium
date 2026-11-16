# unzipper — ZIP / JavaScript

- **Pinned release:** `0.12.5`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** unzipper
- **Local input API:** `Open.buffer(Buffer); entry.buffer()`
- **Documentation:** [API reference](<https://www.npmjs.com/package/unzipper>)
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

Uses Node zlib for DEFLATE; archive parsing is in unzipper.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/javascript/unzipper/README.md)

```sh
python3 parsarium.py build zip javascript unzipper
python3 parsarium.py run zip javascript unzipper controls/zip/hello.zip
```
