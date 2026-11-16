# stream-unzip — ZIP / Python

- **Pinned release:** `0.0.101`
- **License:** MIT
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** stream-unzip native Python parser
- **Local input API:** `stream_unzip.stream_unzip(local byte chunks)`
- **Documentation:** [API reference](<https://github.com/uktrade/stream-unzip>)
- **Catalog evidence:** [parser record](../../../../data/python/zip/parsers.json) · [control verification](../../../../data/python/zip/verification.json) · [within-ecosystem ranking](../../../../data/python/zip/ranking.md)
- **Valid control:** [`controls/zip/hello.zip`](../../../../controls/zip/hello.zip)

## Observed control result

```json
{
  "names": [
    "hello.txt"
  ],
  "hello": "parsarium\n"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/zip/python/stream_unzip/README.md)

```sh
python3 parsarium.py build zip python stream_unzip
python3 parsarium.py run zip python stream_unzip controls/zip/hello.zip
```
