# larzarchive — ZIP / Python

- **Pinned release:** `0.1.0`
- **License:** MIT
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** larzarchive via CPython zipfile
- **Local input API:** `larzarchive.listing(path); extract(path, destination)`
- **Documentation:** [API reference](<https://pypi.org/project/larzarchive/0.1.0/>)
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

[Docker harness and verification receipt](../../../../projects/zip/python/larzarchive/README.md)

```sh
python3 parsarium.py build zip python larzarchive
python3 parsarium.py run zip python larzarchive controls/zip/hello.zip
```
