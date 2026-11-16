# pyzipper — ZIP / Python

- **Pinned release:** `0.4.0`
- **License:** MIT
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** pyzipper fork of CPython zipfile 3.7
- **Local input API:** `pyzipper.AESZipFile(path); namelist(); read()`
- **Documentation:** [API reference](<https://pypi.org/project/pyzipper/0.4.0/>)
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

[Docker harness and verification receipt](../../../../projects/zip/python/pyzipper/README.md)

```sh
python3 parsarium.py build zip python pyzipper
python3 parsarium.py run zip python pyzipper controls/zip/hello.zip
```
