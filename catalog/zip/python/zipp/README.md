# zipp — ZIP / Python

- **Pinned release:** `4.1.2`
- **Upstream:** [source repository](<https://github.com/jaraco/zipp>) · [PyPI](<https://pypi.org/project/zipp/>)
- **License:** MIT
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** zipp via CPython zipfile
- **Local input API:** `zipp.Path(path).iterdir(); read_bytes()`
- **Documentation:** [API reference](<https://zipp.readthedocs.io/en/latest/>)
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

[Docker harness and verification receipt](../../../../projects/zip/python/zipp/README.md)

```sh
python3 parsarium.py build zip python zipp
python3 parsarium.py run zip python zipp controls/zip/hello.zip
```
