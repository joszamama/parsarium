# zipmonkey — ZIP / Python

- **Pinned release:** `1.0.0`
- **License:** MIT
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** zipmonkey via CPython zipfile
- **Local input API:** `zipmonkey.open(path).namelist(); read()`
- **Documentation:** [API reference](<https://pypi.org/project/zipmonkey/1.0.0/>)
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

[Docker harness and verification receipt](../../../../projects/zip/python/zipmonkey/README.md)

```sh
python3 parsarium.py build zip python zipmonkey
python3 parsarium.py run zip python zipmonkey controls/zip/hello.zip
```
