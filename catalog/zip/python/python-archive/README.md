# python-archive — ZIP / Python

- **Pinned release:** `0.2`
- **License:** MIT
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** python-archive via CPython zipfile
- **Local input API:** `archive.Archive(path).extract(destination)`
- **Documentation:** [API reference](<https://pypi.org/project/python-archive/0.2/>)
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

[Docker harness and verification receipt](../../../../projects/zip/python/python_archive/README.md)

```sh
python3 parsarium.py build zip python python_archive
python3 parsarium.py run zip python python_archive controls/zip/hello.zip
```
