# pyunpack — ZIP / Python

- **Pinned release:** `0.3`
- **Upstream:** [source repository](<https://github.com/ponty/pyunpack>) · [PyPI](<https://pypi.org/project/pyunpack/>)
- **License:** BSD-2-Clause
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** pyunpack via CPython zipfile
- **Local input API:** `pyunpack.Archive(path).extractall(destination)`
- **Documentation:** [API reference](<https://pypi.org/project/pyunpack/0.3/>)
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

[Docker harness and verification receipt](../../../../projects/zip/python/pyunpack/README.md)

```sh
python3 parsarium.py build zip python pyunpack
python3 parsarium.py run zip python pyunpack controls/zip/hello.zip
```
