# unzip-stream — ZIP / JavaScript

- **Pinned release:** `0.3.4`
- **License:** MIT
- **Parsed scope:** entries_and_content
- **Underlying family:** unzip-stream
- **Local input API:** `Readable.pipe(unzip.Parse()); async iterate entries`
- **Documentation:** [API reference](<https://www.npmjs.com/package/unzip-stream>)
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

Based on unzip and unzipper, but documents a new streaming engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/javascript/unzip_stream/README.md)

```sh
python3 parsarium.py build zip javascript unzip_stream
python3 parsarium.py run zip javascript unzip_stream controls/zip/hello.zip
```
