# zipfile2 — ZIP / Python

- **Pinned release:** `0.0.12`
- **License:** PSF-2.0
- **Parsed scope:** DEFLATE ZIP entry name and content
- **Underlying family:** zipfile2 CPython zipfile fork
- **Local input API:** `zipfile2.ZipFile(path).namelist(); read()`
- **Documentation:** [API reference](<https://pypi.org/project/zipfile2/0.0.12/>)
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

[Docker harness and verification receipt](../../../../projects/zip/python/zipfile2/README.md)

```sh
python3 parsarium.py build zip python zipfile2
python3 parsarium.py run zip python zipfile2 controls/zip/hello.zip
```
